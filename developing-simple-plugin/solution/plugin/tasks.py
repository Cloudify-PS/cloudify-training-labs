########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


# 'ctx' is always passed as a keyword argument to operations, so
# your operation implementation must either specify it in the arguments
# list, or accept '**kwargs'. Both are shown here.
def my_task(ctx, str1, str2, **kwargs):
    # setting node instance runtime property
    ctx.logger.info("String 1: {}".format(str1))
    ctx.logger.info("String 2: {}".format(str2))
    result = str1 + str2
    ctx.instance.runtime_properties['result'] = result
