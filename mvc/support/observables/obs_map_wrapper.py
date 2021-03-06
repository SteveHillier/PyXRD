# coding=UTF-8
# ex:ts=4:sw=4:et=on
#  -------------------------------------------------------------------------
#  Copyright (C) 2014 by Mathijs Dumon <mathijs dot dumon at gmail dot com>
#  Copyright (C) 2005 by Tobias Weber
#  Copyright (C) 2005 by Roberto Cavada <roboogle@gmail.com>
#
#  mvc is a framework derived from the original pygtkmvc framework
#  hosted at: <http://sourceforge.net/projects/pygtkmvc/>
#
#  mvc is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  mvc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#  -------------------------------------------------------------------------

from .obs_seq_wrapper import ObsSeqWrapper
from .value_wrapper import ValueWrapper

@ValueWrapper.register_wrapper(position=1)
class ObsMapWrapper (ObsSeqWrapper):

    @classmethod
    def wrap_value(cls, label, value, model=None):
        if isinstance(value, dict):
            res = cls(value)
            if model: res.__add_model__(model, label)
            return res

    def __init__(self, m):
        methods = ("clear", "pop", "popitem", "update",
                   "setdefault")
        ObsSeqWrapper.__init__(self, m, methods)
        return
    pass # end of class
