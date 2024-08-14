# (c) 2017, Ansible by RedHat Inc,
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

#############################################
from __future__ import annotations

from ansible.utils.vars import combine_vars
import logging


def sort_groups(groups):
    return sorted(groups, key=lambda g: (g.depth, g.priority, g.name))


def get_group_vars(groups, log=False):
    """
    Combine all the group vars from a list of inventory groups.

    :param groups: list of ansible.inventory.group.Group objects
    :param log: boolean, if True, log the combination process
    :rtype: dict
    """
    results = {}
    logger = logging.getLogger(__name__)
    
    for group in sort_groups(groups):
        if log:
            logger.info(f"Combining vars from group: {group.name}")
        results = combine_vars(results, group.get_vars())

    if log:
        logger.info(f"Final combined vars: {results}")
    
    return results
