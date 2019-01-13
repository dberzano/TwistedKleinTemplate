# This file is part of Twisted Klein webapp template.
# Author: Dario Berzano <dario.berzano@gmail.com>
#
# Twisted Klein webapp template is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# Twisted Klein webapp template is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Twisted Klein webapp
# template. If not, see <http://www.gnu.org/licenses/>.

"""Utilities to the Twisted Klein webapp template.
"""

def get_form(req, label, var_type=str, get_list=False):
    """Get elements from a form in an intuitive way. `label` is a string. If `type` is not specified
    the value of the first element from the form list is returned (use `type=list` to return the
    whole list). If `type` is `bool` then some smart comparison on strings meaning `True` is
    performed.
    """
    if isinstance(label, str):
        label = label.encode()  # to bytes
    val = []
    for i in req.args.get(label, [b"off"]) if var_type == bool else req.args[label]:
        i = i.decode("utf-8")  # to string
        if var_type == bool:
            i = i.lower() in ["on", "true", "yes", "1"]
        val.append(i)
    return val if get_list else val[0]
