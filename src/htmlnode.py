class HTMLNode():
	def __init__(self, tag=None, value=None, children=None, props=None):
		if props is not None and not isinstance(props, dict):
			raise TypeError("props must be dictionary")
		if children is not None and not isinstance(children, list):
			raise TypeError("children must be list")
		if value is not None and not isinstance(value, str):
			raise TypeError("value must be string")
		if tag is not None and not isinstance(tag, str):
			raise TypeError("tag must be string")
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError("to_html method not implemented")

	def props_to_html(self):
		if self.props is None:
			return ""
		return "".join(list(map(lambda key: f' {key}="{self.props[key]}"',
				self.props)))

	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
	
class LeafNode(HTMLNode):
	def __init__(self, tag=None, value=None, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value == None:
			raise ValueError("leaf node must have a value")
		if self.tag == None:
			return self.value
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
	
	def __repr__(self):
		return f"LeafNode({self.tag}, {self.value}, {self.props})"
