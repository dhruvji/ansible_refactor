import re
import itertools
from ansible.module_utils.six import string_types
from ansible.parsing.utils.addresses import parse_address
from ansible.module_utils.common.text.converters import to_text


def order_patterns(patterns):
    ''' takes a list of patterns and reorders them by modifier to apply them consistently '''

    pattern_regular = []
    pattern_intersection = []
    pattern_exclude = []
    for p in patterns:
        if not p:
            continue

        if p[0] == "!":
            pattern_exclude.append(p)
        elif p[0] == "&":
            pattern_intersection.append(p)
        else:
            pattern_regular.append(p)

    if pattern_regular == []:
        pattern_regular = ['all']

    return pattern_regular + pattern_intersection + pattern_exclude

def split_host_pattern(pattern):
    """
    Takes a string containing host patterns separated by commas (or a list
    thereof) and returns a list of single patterns (which may not contain
    commas). Whitespace is ignored.

    Also accepts ':' as a separator for backwards compatibility, but it is
    not recommended due to the conflict with IPv6 addresses and host ranges.
    """

    if isinstance(pattern, list):
        results = (split_host_pattern(p) for p in pattern)
        return list(itertools.chain.from_iterable(results))
    elif not isinstance(pattern, string_types):
        pattern = to_text(pattern, errors='surrogate_or_strict')

    if u',' in pattern:
        patterns = pattern.split(u',')

    else:
        try:
            (base, port) = parse_address(pattern, allow_ranges=True)
            patterns = [pattern]
        except Exception:
            patterns = re.findall(
                to_text(r'''(?:     
                        [^\s:\[\]]  
                        |           
                        \[[^\]]*\]  
                    )+              
                '''), pattern, re.X
            )

    return [p.strip() for p in patterns if p.strip()]
