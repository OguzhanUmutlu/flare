import hashlib
from math import inf

import re._constants as sre_constants  # noqa
import re._parser as sre_parse  # noqa

from .core import LazyOp, addr
from .nbt import nbt
from .score import score
from .. import context as ctx, nbtbytearray, nbtcompound, nbtlist
from ..context import _runcmd
from ..control_flow import ScoreIfMatches, _flare_if
from ..types import NBTType


def _init_globals():
    global regex_matched, current_char, char_valid, regex_index, regex_target, macro_args
    global in_match, category_match, prev_is_word, curr_is_word, is_bol, is_eol
    global ref_start, ref_end, ref_match, target_char, assert_not_failed, temp_end
    global temp_start, temp_prev_idx, prev_idx, regex_stack

    regex_matched = score(addr="!regex_matched")
    current_char = score(addr="!regex_current_char")
    char_valid = score(addr="!regex_char_valid")
    regex_index = score(addr="!regex_index")
    regex_target = nbtbytearray(addr="flare:regex target")
    macro_args = nbtcompound(addr="flare:regex macro_args")
    in_match = score(addr="!regex_in_match")
    category_match = score(addr="!regex_category_match")
    prev_is_word = score(addr="!regex_prev_is_word")
    curr_is_word = score(addr="!regex_curr_is_word")
    is_bol = score(addr="!regex_is_bol")
    is_eol = score(addr="!regex_is_eol")
    ref_start = score(addr="!regex_ref_start")
    ref_end = score(addr="!regex_ref_end")
    ref_match = score(addr="!regex_ref_match")
    target_char = score(addr="!regex_target_char")
    assert_not_failed = score(addr="!regex_assert_not_failed")
    temp_end = score(addr="!regex_temp_end")
    temp_start = score(addr="!regex_temp_start")
    temp_prev_idx = score(addr="!regex_temp_prev_idx")
    prev_idx = score(addr="!regex_prev_idx")
    regex_stack = nbtlist(addr="flare:regex stack")


def _get_group_start(group_num):
    return score(addr=f"!regex_group_{group_num}_start")


def _get_group_end(group_num):
    return score(addr=f"!regex_group_{group_num}_end")


_read_char_emitted = False


def _emit_read_char():
    global _read_char_emitted
    func_name = f"{ctx._current_namespace}:__flare_regex_read_char"
    if not _read_char_emitted:
        _read_char_emitted = True
        with ctx.push_context(func_name):
            _runcmd(
                f"$execute store success score {addr(char_valid)} store result score {addr(current_char)} run data get {addr(regex_target)}[$(idx)]")
    return func_name


def _compile_node(node: tuple, next_func: str | None, base_name: str, needs_capture=False):
    op, val = node
    func_name = f"{base_name}_{ctx.next_func_id()}"

    with ctx.push_context(func_name):
        ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

        if op == sre_constants.LITERAL:
            char_val = val

            current_char[:] = -999
            char_valid[:] = 0

            macro_args.idx = regex_index
            _runcmd(f"function {_emit_read_char()} with {addr(macro_args)}")

            ScoreIfMatches(char_valid, 0).then(lambda: _runcmd("return 0"))
            ScoreIfMatches(current_char, char_val).invert().then(lambda: _runcmd(f"return 0"))

            regex_index.__iadd__(1)
            if next_func:
                _runcmd(f"function {next_func}")
            else:
                regex_matched[:] = 1

            ScoreIfMatches(regex_matched, 0).then(lambda: regex_index.__isub__(1))

        elif op == sre_constants.IN:
            current_char[:] = -999
            char_valid[:] = 0
            macro_args.idx = regex_index
            _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")

            ScoreIfMatches(char_valid, 0).then(lambda: _runcmd("return 0"))

            in_match[:] = 0

            negate = False
            if len(val) > 0 and val[0][0] == sre_constants.NEGATE:
                negate = True
                val = val[1:]

            for sub_op, sub_val in val:
                if sub_op == sre_constants.LITERAL:
                    ScoreIfMatches(current_char, sub_val).then(lambda: in_match.__iset__(1))
                elif sub_op == sre_constants.RANGE:
                    start, end = sub_val
                    ScoreIfMatches(current_char, (start, end)).then(lambda: in_match.__iset__(1))
                elif sub_op == sre_constants.CATEGORY:
                    if sub_val == sre_constants.CATEGORY_DIGIT:
                        ScoreIfMatches(current_char, (48, 57)).then(lambda: in_match.__iset__(1))
                    elif sub_val == sre_constants.CATEGORY_NOT_DIGIT:
                        ScoreIfMatches(current_char, (48, 57)).invert().then(lambda: in_match.__iset__(1))
                    elif sub_val == sre_constants.CATEGORY_SPACE:
                        ScoreIfMatches(current_char, (9, 10)).then(lambda: in_match.__iset__(1))
                        ScoreIfMatches(current_char, 13).then(lambda: in_match.__iset__(1))
                        ScoreIfMatches(current_char, 32).then(lambda: in_match.__iset__(1))
                    elif sub_val == sre_constants.CATEGORY_NOT_SPACE:
                        _flare_if(lambda: (current_char != 9) & (current_char != 10) & (current_char != 13) & (
                                current_char != 32), lambda: in_match.__iset__(1))
                    elif sub_val == sre_constants.CATEGORY_WORD:
                        ScoreIfMatches(current_char, (97, 122)).then(lambda: in_match.__iset__(1))
                        ScoreIfMatches(current_char, (65, 90)).then(lambda: in_match.__iset__(1))
                        ScoreIfMatches(current_char, (48, 57)).then(lambda: in_match.__iset__(1))
                        ScoreIfMatches(current_char, 95).then(lambda: in_match.__iset__(1))
                    elif sub_val == sre_constants.CATEGORY_NOT_WORD:
                        _flare_if(lambda: (current_char < 97) | (current_char > 122), lambda:
                        _flare_if(lambda: (current_char < 65) | (current_char > 90), lambda:
                        _flare_if(lambda: (current_char < 48) | (current_char > 57), lambda:
                        _flare_if(lambda: current_char != 95, lambda: in_match.__iset__(1)))))

            if negate:
                ScoreIfMatches(in_match, 1).then(lambda: _runcmd("return 0"))
            else:
                ScoreIfMatches(in_match, 0).then(lambda: _runcmd("return 0"))

            regex_index.__iadd__(1)
            if next_func:
                _runcmd(f"function {next_func}")
            else:
                regex_matched[:] = 1

            ScoreIfMatches(regex_matched, 0).then(lambda: regex_index.__isub__(1))

        elif op == sre_constants.NOT_LITERAL:
            char_val = val

            current_char[:] = -999
            char_valid[:] = 0
            macro_args.idx = regex_index
            _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")

            ScoreIfMatches(char_valid, 0).then(lambda: _runcmd("return 0"))
            ScoreIfMatches(current_char, char_val).then(lambda: _runcmd(f"return 0"))

            regex_index.__iadd__(1)
            if next_func:
                _runcmd(f"function {next_func}")
            else:
                regex_matched[:] = 1

            ScoreIfMatches(regex_matched, 0).then(lambda: regex_index.__isub__(1))

        elif op == sre_constants.CATEGORY:
            current_char[:] = -999
            char_valid[:] = 0
            macro_args.idx = regex_index
            _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")

            ScoreIfMatches(char_valid, 0).then(lambda: _runcmd("return 0"))

            category_match[:] = 0
            if val == sre_constants.CATEGORY_DIGIT:
                ScoreIfMatches(current_char, (48, 57)).then(lambda: category_match.__iset__(1))
            elif val == sre_constants.CATEGORY_NOT_DIGIT:
                ScoreIfMatches(current_char, (48, 57)).invert().then(lambda: category_match.__iset__(1))
            elif val == sre_constants.CATEGORY_SPACE:
                ScoreIfMatches(current_char, 9).then(lambda: category_match.__iset__(1))
                ScoreIfMatches(current_char, 10).then(lambda: category_match.__iset__(1))
                ScoreIfMatches(current_char, 13).then(lambda: category_match.__iset__(1))
                ScoreIfMatches(current_char, 32).then(lambda: category_match.__iset__(1))
            elif val == sre_constants.CATEGORY_NOT_SPACE:
                _flare_if(
                    lambda: (current_char != 9) & (current_char != 10) & (current_char != 13) & (current_char != 32),
                    lambda: category_match.__iset__(1))
            elif val == sre_constants.CATEGORY_WORD:
                ScoreIfMatches(current_char, (97, 122)).then(lambda: category_match.__iset__(1))
                ScoreIfMatches(current_char, (65, 90)).then(lambda: category_match.__iset__(1))
                ScoreIfMatches(current_char, (48, 57)).then(lambda: category_match.__iset__(1))
                ScoreIfMatches(current_char, 95).then(lambda: category_match.__iset__(1))
            elif val == sre_constants.CATEGORY_NOT_WORD:
                _flare_if(lambda: (current_char < 97) | (current_char > 122), lambda:
                _flare_if(lambda: (current_char < 65) | (current_char > 90), lambda:
                _flare_if(lambda: (current_char < 48) | (current_char > 57), lambda:
                _flare_if(lambda: current_char != 95, lambda: category_match.__iset__(1)))))

            ScoreIfMatches(category_match, 0).then(lambda: _runcmd("return 0"))

            regex_index.__iadd__(1)
            if next_func:
                _runcmd(f"function {next_func}")
            else:
                regex_matched[:] = 1

            ScoreIfMatches(regex_matched, 0).then(lambda: regex_index.__isub__(1))

        elif op == sre_constants.BRANCH:
            _, branches = val
            for branch_nodes in branches:
                branch_func = _compile_sequence(branch_nodes, next_func, f"{base_name}_branch", needs_capture)
                _runcmd(f"function {branch_func}")
                ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

        elif op == sre_constants.MAX_REPEAT:
            min_repeats, max_repeats, subnodes = val

            node_id = ctx.next_func_id()
            loop_func = f"{base_name}_max_repeat_loop_{node_id}"
            counter_name = f"!loop_{node_id}"

            sub_start = _compile_sequence(subnodes, loop_func, f"{base_name}_sub_{node_id}", needs_capture)

            with ctx.push_context(loop_func):
                ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

                temp_prev_idx[:] = regex_stack[-2]
                _flare_if(lambda: regex_index == temp_prev_idx,
                          lambda: _runcmd(f"function {next_func if next_func else 'flare:regex_dummy_match'}"))
                _flare_if(lambda: (regex_index == temp_prev_idx) & (regex_matched == 1),
                          lambda: _runcmd("return 1"))
                _flare_if(lambda: regex_index == temp_prev_idx, lambda: _runcmd("return 0"))

                score(addr=f"{counter_name}").__iadd__(1)

                if max_repeats != sre_constants.MAXREPEAT:
                    ScoreIfMatches(score(addr=f"{counter_name}"), max_repeats).then(
                        lambda: _runcmd(f"function {next_func if next_func else 'flare:regex_dummy_match'}"))
                    ScoreIfMatches(score(addr=f"{counter_name}"), max_repeats).then(lambda: _runcmd("return 0"))

                regex_stack.append(0)
                regex_stack[-1] = regex_index

                regex_stack.append(0)
                regex_stack[-1] = score(addr=f"{counter_name}")

                _runcmd(f"function {sub_start}")
                ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

                score(addr=f"{counter_name}")[:] = regex_stack[-1]
                regex_stack[-1].remove()
                regex_index[:] = regex_stack[-1]
                regex_stack[-1].remove()

                ScoreIfMatches(score(addr=f"{counter_name}"), (min_repeats, inf)).then(
                    lambda: _runcmd(f"function {next_func if next_func else 'flare:regex_dummy_match'}"))

            score(addr=f"{counter_name}")[:] = 0

            regex_stack.append(0)
            regex_stack[-1] = regex_index

            regex_stack.append(0)
            regex_stack[-1] = score(addr=f"{counter_name}")

            _runcmd(f"function {sub_start}")
            ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

            score(addr=f"{counter_name}")[:] = regex_stack[-1]
            regex_stack[-1].remove()
            regex_index[:] = regex_stack[-1]
            regex_stack[-1].remove()

            ScoreIfMatches(score(addr=f"{counter_name}"), (min_repeats, inf)).then(
                lambda: _runcmd(f"function {next_func if next_func else 'flare:regex_dummy_match'}"))

        elif op == sre_constants.MIN_REPEAT:
            min_repeats, max_repeats, subnodes = val

            node_id = ctx.next_func_id()
            loop_func = f"{base_name}_min_repeat_loop_{node_id}"
            counter_name = f"!loop_{node_id}"

            sub_start = _compile_sequence(subnodes, loop_func, f"{base_name}_sub_{node_id}", needs_capture)

            with ctx.push_context(loop_func):
                ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

                temp_prev_idx[:] = regex_stack[-2]
                _flare_if(lambda: regex_index == temp_prev_idx,
                          lambda: _runcmd(f"function {next_func if next_func else 'flare:regex_dummy_match'}"))
                _flare_if(lambda: (regex_index == temp_prev_idx) & (regex_matched == 1),
                          lambda: _runcmd("return 1"))
                _flare_if(lambda: regex_index == temp_prev_idx, lambda: _runcmd("return 0"))

                score(addr=f"{counter_name}").__iadd__(1)

                ScoreIfMatches(score(addr=f"{counter_name}"), (min_repeats, inf)).then(
                    lambda: _runcmd(f"function {next_func if next_func else 'flare:regex_dummy_match'}"))
                ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

                if max_repeats != sre_constants.MAXREPEAT:
                    ScoreIfMatches(score(addr=f"{counter_name}"), max_repeats).then(lambda: _runcmd("return 0"))

                regex_stack.append(0)
                regex_stack[-1] = regex_index
                regex_stack.append(0)
                regex_stack[-1] = score(addr=f"{counter_name}")

                _runcmd(f"function {sub_start}")
                ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

                score(addr=f"{counter_name}")[:] = regex_stack[-1]
                regex_stack[-1].remove()
                regex_index[:] = regex_stack[-1]
                regex_stack[-1].remove()

            score(addr=f"{counter_name}")[:] = 0

            ScoreIfMatches(score(addr=f"{counter_name}"), (min_repeats, inf)).then(
                lambda: _runcmd(f"function {next_func if next_func else 'flare:regex_dummy_match'}"))
            ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

            if max_repeats != 0:
                regex_stack.append(0)
                regex_stack[-1] = regex_index
                regex_stack.append(0)
                regex_stack[-1] = score(addr=f"{counter_name}")

                _runcmd(f"function {sub_start}")
                ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

                score(addr=f"{counter_name}")[:] = regex_stack[-1]
                regex_stack[-1].remove()
                regex_index[:] = regex_stack[-1]
                regex_stack[-1].remove()

        elif op == sre_constants.ANY:
            current_char[:] = -999
            char_valid[:] = 0
            macro_args.idx = regex_index
            _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")

            ScoreIfMatches(char_valid, 0).then(lambda: _runcmd("return 0"))
            ScoreIfMatches(current_char, 10).then(lambda: _runcmd("return 0"))

            regex_index.__iadd__(1)
            if next_func:
                _runcmd(f"function {next_func}")
            else:
                regex_matched[:] = 1

            ScoreIfMatches(regex_matched, 0).then(lambda: regex_index.__isub__(1))

        elif op == sre_constants.AT:
            if val in (sre_constants.AT_BEGINNING, sre_constants.AT_BEGINNING_STRING):
                macro_args.idx = regex_index
                ScoreIfMatches(regex_index, 0).invert().then(lambda: _runcmd("return 0"))
                if next_func:
                    _runcmd(f"function {next_func}")
                else:
                    regex_matched[:] = 1
            elif val in (sre_constants.AT_END, sre_constants.AT_END_STRING):
                char_valid[:] = 0
                macro_args.idx = regex_index
                _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")
                ScoreIfMatches(char_valid, 0).invert().then(lambda: _runcmd("return 0"))
                if next_func:
                    _runcmd(f"function {next_func}")
                else:
                    regex_matched[:] = 1
            elif val in (sre_constants.AT_BOUNDARY, sre_constants.AT_NON_BOUNDARY):
                is_boundary = 1 if val == sre_constants.AT_BOUNDARY else 0

                char_valid[:] = 0
                prev_idx[:] = regex_index
                prev_idx.__isub__(1)
                macro_args.idx = prev_idx
                _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")
                prev_is_word[:] = 0
                (ScoreIfMatches(char_valid, 0).invert() & ScoreIfMatches(current_char, (97, 122))).then(
                    lambda: prev_is_word.__iset__(1))
                (ScoreIfMatches(char_valid, 0).invert() & ScoreIfMatches(current_char, (65, 90))).then(
                    lambda: prev_is_word.__iset__(1))
                (ScoreIfMatches(char_valid, 0).invert() & ScoreIfMatches(current_char, (48, 57))).then(
                    lambda: prev_is_word.__iset__(1))
                (ScoreIfMatches(char_valid, 0).invert() & ScoreIfMatches(current_char, 95)).then(
                    lambda: prev_is_word.__iset__(1))

                char_valid[:] = 0
                macro_args.idx = regex_index
                _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")
                curr_is_word[:] = 0
                (ScoreIfMatches(char_valid, 0).invert() & ScoreIfMatches(current_char, (97, 122))).then(
                    lambda: curr_is_word.__iset__(1))
                (ScoreIfMatches(char_valid, 0).invert() & ScoreIfMatches(current_char, (65, 90))).then(
                    lambda: curr_is_word.__iset__(1))
                (ScoreIfMatches(char_valid, 0).invert() & ScoreIfMatches(current_char, (48, 57))).then(
                    lambda: curr_is_word.__iset__(1))
                (ScoreIfMatches(char_valid, 0).invert() & ScoreIfMatches(current_char, 95)).then(
                    lambda: curr_is_word.__iset__(1))

                if is_boundary:
                    _flare_if(lambda: prev_is_word == curr_is_word, lambda: _runcmd("return 0"))
                else:
                    _flare_if(lambda: prev_is_word != curr_is_word, lambda: _runcmd("return 0"))

                if next_func:
                    _runcmd(f"function {next_func}")
                else:
                    regex_matched[:] = 1
            elif val in (sre_constants.AT_BEGINNING_LINE, sre_constants.AT_END_LINE):
                if val == sre_constants.AT_BEGINNING_LINE:
                    is_bol[:] = 0
                    ScoreIfMatches(regex_index, 0).then(lambda: is_bol.__iset__(1))
                    prev_idx[:] = regex_index
                    prev_idx.__isub__(1)
                    macro_args.idx = prev_idx
                    _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")
                    (ScoreIfMatches(char_valid, 0).invert() & ScoreIfMatches(current_char, 10)).then(
                        lambda: is_bol.__iset__(1))
                    ScoreIfMatches(is_bol, 0).then(lambda: _runcmd("return 0"))
                else:
                    is_eol[:] = 0
                    macro_args.idx = regex_index
                    char_valid[:] = 0
                    _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")
                    (ScoreIfMatches(char_valid, 0).invert() & ScoreIfMatches(current_char, 10)).then(
                        lambda: is_eol.__iset__(1))
                    ScoreIfMatches(is_eol, 0).then(lambda: _runcmd("return 0"))

                if next_func:
                    _runcmd(f"function {next_func}")
                else:
                    regex_matched[:] = 1
            else:
                raise NotImplementedError(f"Regex AT anchor {val} not yet supported in Flare.")

        elif op == sre_constants.SUBPATTERN:
            group_num, add_flags, del_flags, subnodes = val

            if not needs_capture:
                sub_func = _compile_sequence(subnodes, next_func, f"{base_name}_subpat_{group_num}", needs_capture)
                _runcmd(f"function {sub_func}")
            else:
                pass

        elif op == sre_constants.GROUPREF:
            group_num = val

            node_id = ctx.next_func_id()
            loop_func = f"{base_name}_groupref_loop_{node_id}"

            ref_start[:] = _get_group_start(group_num)
            ref_end[:] = _get_group_end(group_num)

            ref_match[:] = 1

            with ctx.push_context(loop_func):
                ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

                _flare_if(lambda: ref_start >= ref_end,
                          lambda: _runcmd(f"function {next_func if next_func else 'flare:regex_dummy_match'}"))
                _flare_if(lambda: ref_start >= ref_end, lambda: _runcmd(f"return 0"))

                char_valid[:] = 0
                macro_args.idx = regex_index
                _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")
                ScoreIfMatches(char_valid, 0).then(lambda: _runcmd("return 0"))
                target_char[:] = current_char

                char_valid[:] = 0
                macro_args.idx = ref_start
                _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")

                _flare_if(lambda: target_char != current_char, lambda: _runcmd(f"return 0"))

                regex_index.__iadd__(1)
                ref_start.__iadd__(1)
                _runcmd(f"function {loop_func}")

                ScoreIfMatches(regex_matched, 0).then(lambda: regex_index.__isub__(1))

            _runcmd(f"function {loop_func}")

        elif op == sre_constants.ASSERT:
            direction, subnodes = val
            node_id = ctx.next_func_id()
            wrapper_func = f"{base_name}_assert_wrap_{node_id}"

            sub_start = _compile_sequence(subnodes, wrapper_func, f"{base_name}_sub_{node_id}", needs_capture)

            with ctx.push_context(wrapper_func):
                ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

                score(addr=f"orig_idx_{node_id}")[:] = regex_stack[-1]
                score(addr=f"adv_idx_{node_id}")[:] = regex_index
                regex_index[:] = score(addr=f"orig_idx_{node_id}")

                if next_func:
                    _runcmd(f"function {next_func}")
                else:
                    regex_matched[:] = 1

                ScoreIfMatches(regex_matched, 0).then(lambda: regex_index.__iset__(score(addr=f"adv_idx_{node_id}")))

            regex_stack.append(0)
            regex_stack[-1] = regex_index

            _runcmd(f"function {sub_start}")

            ScoreIfMatches(regex_matched, 0).then(lambda: regex_index.__iset__(regex_stack[-1]))
            ScoreIfMatches(regex_matched, 0).then(lambda: regex_stack[-1].remove())

        elif op == sre_constants.ASSERT_NOT:
            direction, subnodes = val
            node_id = ctx.next_func_id()

            terminal_func = f"{base_name}_assertnot_term_{node_id}"
            with ctx.push_context(terminal_func):
                regex_matched[:] = 1

            sub_start = _compile_sequence(subnodes, terminal_func, f"{base_name}_sub_{node_id}", needs_capture)

            regex_stack.append(0)
            regex_stack[-1] = regex_index

            _runcmd(f"function {sub_start}")

            assert_not_failed[:] = 0
            ScoreIfMatches(regex_matched, 1).then(lambda: assert_not_failed.__iset__(1))

            regex_matched[:] = 0

            regex_index[:] = regex_stack[-1]
            regex_stack[-1].remove()

            ScoreIfMatches(assert_not_failed, 0).then(
                lambda: _runcmd(f"function {next_func if next_func else 'flare:regex_dummy_match'}"))
            (ScoreIfMatches(assert_not_failed, 0) & ScoreIfMatches(regex_matched, 1)).then(
                lambda: _runcmd(f"return 1"))
        else:
            raise NotImplementedError(f"Regex opcode {op} not yet supported in Flare.")

    return func_name


def _compile_sequence(nodes, final_continuation: str, base_name: str, needs_capture=False):
    current_cont = final_continuation
    for i in reversed(range(len(nodes))):
        if needs_capture and nodes[i][0] == sre_constants.SUBPATTERN:
            group_num, add_flags, del_flags, subnodes = nodes[i][1]
            node_id = ctx.next_func_id()

            sub_end_func = f"{base_name}_subend_{node_id}"
            with ctx.push_context(sub_end_func):
                _get_group_end(group_num)[:] = regex_index
                if current_cont:
                    _runcmd(f"function {current_cont}")
                else:
                    regex_matched[:] = 1

            inner_start = _compile_sequence(subnodes, sub_end_func, f"{base_name}_subpat_{group_num}", needs_capture)

            sub_start_func = f"{base_name}_substart_{node_id}"
            with ctx.push_context(sub_start_func):
                ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

                regex_stack.append(-1)
                regex_stack[-1] = _get_group_start(group_num)
                regex_stack.append(-1)
                regex_stack[-1] = _get_group_end(group_num)

                _get_group_start(group_num)[:] = regex_index

                _runcmd(f"function {inner_start}")
                ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

                temp_end[:] = regex_stack[-1]
                _get_group_end(group_num).__iset__(temp_end)
                regex_stack[-1].remove()

                temp_start[:] = regex_stack[-1]
                _get_group_start(group_num).__iset__(temp_start)
                regex_stack[-1].remove()

            current_cont = sub_start_func

        else:
            current_cont = _compile_node(nodes[i], current_cont, base_name, needs_capture)

    return current_cont


def _needs_capture(ast):
    for op, val in ast:
        if op == sre_constants.GROUPREF:
            return True
        elif op in (sre_constants.SUBPATTERN, sre_constants.BRANCH, sre_constants.MAX_REPEAT, sre_constants.MIN_REPEAT,
                    sre_constants.ASSERT, sre_constants.ASSERT_NOT):
            if op == sre_constants.SUBPATTERN:
                if val[0] is not None:
                    return True
                if _needs_capture(val[3]): return True
            elif op == sre_constants.BRANCH:
                for b in val[1]:
                    if _needs_capture(b): return True
            else:
                if _needs_capture(val[-1]): return True
    return False


def compile_regex(pattern, flags=0, capture=False):
    _init_globals()
    cache_key = (pattern, flags)
    if cache_key in ctx._regex_cache:
        return ctx._regex_cache[cache_key]

    ast = sre_parse.parse(pattern, flags)

    needs_capture = capture or _needs_capture(ast)

    unique_id = hashlib.md5(pattern.encode()).hexdigest()[:8]
    base_name = f"{ctx._current_namespace}:regex_{unique_id}"

    terminal_func = f"{base_name}_terminal"
    with ctx.push_context(terminal_func):
        regex_matched[:] = 1
        _get_group_end(0)[:] = regex_index

    start_func = _compile_sequence(ast, terminal_func, base_name, needs_capture)

    search_func = f"{base_name}_search"
    with ctx.push_context(search_func):
        ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))
        _get_group_start(0)[:] = regex_index
        _runcmd(f"function {start_func}")
        ScoreIfMatches(regex_matched, 1).then(lambda: _runcmd("return 1"))

        current_char[:] = -999
        char_valid[:] = 0
        macro_args.idx = regex_index
        _runcmd(f"function {_emit_read_char()} with storage flare:regex macro_args")

        ScoreIfMatches(char_valid, 0).invert().then(lambda: regex_index.__iadd__(1))
        ScoreIfMatches(char_valid, 0).invert().then(lambda: _runcmd(f"function {search_func}"))

    pat = FlareRegexPattern(pattern, flags, start_func, search_func)
    ctx._regex_cache[cache_key] = pat
    return pat


import re as _std_re

_orig_match = _std_re.match
_orig_search = _std_re.search
_orig_compile = _std_re.compile


class RegexMatch(LazyOp):
    def __init__(self, target, eval_fn, alloc_temp_fn=None, make_copy_fn=None):
        super().__init__(target, eval_fn, alloc_temp_fn, make_copy_fn)
        self.target = target

    def group(self, index=0):
        start = _get_group_start(index)
        end = _get_group_end(index)
        return self.target[start:end]

    def __icopy__(self, varid: str, is_recursive: bool = False):
        t = super().__icopy__(varid)
        t.group = self.group
        t.target = self.target
        return t


class FlareRegexPattern:
    def __init__(self, pattern, flags, start_func, start_func_search):
        self.pattern = pattern
        self.flags = flags
        self.start_func = start_func
        self.start_func_search = start_func_search
        self._std_pat = _orig_compile(pattern, flags)

    def __getattr__(self, item):
        return getattr(self._std_pat, item)

    def match(self, target):
        from .core import FlareValue
        if not isinstance(target, FlareValue):
            return self._std_pat.match(target)

        if target._type != NBTType.String:
            raise TypeError("Regex target must be an NBT String.")

        def eval_match(dest):
            _init_globals()
            temp_byte_array = nbt(addr=f"flare:temp regex_bytes_{ctx.next_temp_id()}", datatype=NBTType.ByteArray)
            temp_byte_array[:] = target.to_ascii()
            regex_matched[:] = 0
            regex_index[:] = 0
            _get_group_start(0)[:] = 0
            regex_target[:] = temp_byte_array
            _runcmd(f"function {self.start_func}")
            dest[:] = regex_matched
            return dest

        return RegexMatch(target, eval_match, lambda: score(addr=f"!regex_out_{ctx.next_temp_id()}"),
                          lambda varid: score(addr=f"{varid} {ctx.vars_obj}"))

    def search(self, target):
        from .core import FlareValue
        if not isinstance(target, FlareValue):
            return self._std_pat.search(target)

        if target._type != NBTType.String:
            raise TypeError("Regex target must be an NBT String.")

        def eval_search(dest):
            _init_globals()
            temp_byte_array = nbt(addr=f"flare:temp regex_bytes_{ctx.next_temp_id()}", datatype=NBTType.ByteArray)
            temp_byte_array[:] = target.to_ascii()
            regex_matched[:] = 0
            regex_index[:] = 0
            regex_target[:] = temp_byte_array
            _runcmd(f"function {self.start_func_search}")
            dest[:] = regex_matched
            return dest

        return RegexMatch(target, eval_search, lambda: score(addr=f"!regex_out_{ctx.next_temp_id()}"),
                          lambda varid: score(addr=f"{varid} {ctx.vars_obj}"))


def _flare_match(pattern, string, flags=0):
    from .core import FlareValue
    if isinstance(string, FlareValue):
        return compile_regex(pattern, flags).match(string)
    return _orig_match(pattern, string, flags)


def _flare_search(pattern, string, flags=0):
    from .core import FlareValue
    if isinstance(string, FlareValue):
        return compile_regex(pattern, flags).search(string)
    return _orig_search(pattern, string, flags)


_std_re.match = _flare_match
_std_re.search = _flare_search


class re_patch:
    @staticmethod
    def compile(pattern, flags=0):
        return compile_regex(pattern, flags)

    @staticmethod
    def match(pattern, string, flags=0):
        return _flare_match(pattern, string, flags)

    @staticmethod
    def search(pattern, string, flags=0):
        return _flare_search(pattern, string, flags)
