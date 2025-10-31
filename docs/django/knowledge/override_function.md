### 基于类的视图（Class-Based Views）提供了许多可以重写的方法，以便自定义视图的行为。

* get_queryset: 用于指定视图所使用的查询集。默认返回模型的全部数据，通过重写可以过滤、排序等。

* get_context_data: 用于向模板传递额外的上下文数据。

* get: 处理GET请求的方法，可以重写以自定义GET请求的处理逻辑。

* post: 处理POST请求的方法。

* form_valid: 在表单验证通过时调用，可以在此处添加自定义逻辑（如保存对象时附加其他属性）。

* form_invalid: 在表单验证失败时调用。

* dispatch: 请求首先进入的方法，可以根据请求方法（GET、POST等）分发到对应的方法，也可以在此处进行一些初始操作。

* get_object: 获取单个对象（用于DetailView、UpdateView等）。

* get_success_url: 定义表单处理成功后重定向的URL。

* get_form_class: 获取表单类，可以动态选择表单。

* get_form_kwargs: 获取传递给表单的关键字参数。

* get_template_names: 动态选择模板。

* get_paginate_by: 动态设置分页大小。

* get_ordering: 动态设置排序。

* get_context_object_name: 设置上下文对象名称。

### 常用重写方法总结表
|  方法名  |  视图类型  |  作用  |  使用频率  |
|  ----  | ----  | ----  | ----  |
|get_queryset()	|所有	|自定义数据查询逻辑	|⭐⭐⭐⭐⭐
|get_context_data()	|所有	|添加模板上下文数据	|⭐⭐⭐⭐⭐
|get_object()	|DetailView, UpdateView	|自定义单个对象获取	|⭐⭐⭐⭐
|form_valid()	|CreateView, UpdateView	|表单验证成功处理	|⭐⭐⭐⭐
|get_form_class()	|表单视图	|动态选择表单类	|⭐⭐⭐
|get_form_kwargs()	|表单视图	|自定义表单参数	|⭐⭐⭐
|get_success_url()	|表单视图	|自定义成功跳转URL	|⭐⭐⭐
|dispatch()	|所有	|请求预处理和权限检查	|⭐⭐⭐
|get()	|所有	|自定义GET请求处理	|⭐⭐
|post()	|所有	|自定义POST请求处理	|⭐⭐
#### 最佳实践建议
* 总是调用 super()：在重写方法时，确保调用父类方法

* 合理使用查询优化：在 get_queryset() 中使用 select_related() 和 prefetch_related()

* 保持方法单一职责：每个重写方法只负责一个明确的功能

* 使用消息框架：在表单处理中给用户反馈

* 考虑权限控制：在 dispatch() 或 get() 中进行权限检查

