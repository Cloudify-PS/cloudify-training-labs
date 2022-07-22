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
from cloudify.decorators import workflow
from cloudify.workflows import ctx

@workflow
def uppercase(ctx, log_output, **kwargs):
    graph = ctx.graph_mode()

    for node in ctx.nodes:
        if "test.nodes.Concat" in node.type_hierarchy:
            for instance in node.instances:
                operation = "test.interfaces.operations.upper"

                graph.add_task(instance.execute_operation(operation, kwargs={"log_output": log_output}, allow_kwargs_override=True))

    return graph.execute()
