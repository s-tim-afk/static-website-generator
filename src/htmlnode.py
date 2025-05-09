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
		if value is None:
			raise ValueError("LeafNode must have a value")
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.tag == None:
			return self.value
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
	
	def __repr__(self):
		return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		if tag is None:
			raise ValueError("ParentNode must have a tag")
		if children is None:
			raise ValueError("ParentNode must have children")
		super().__init__(tag, None, children, props)

	def to_html(self):
		return f"<{self.tag}{self.props_to_html()}>{''.join(
			list(
				map(lambda child: child.to_html(), self.children)))}</{self.tag}>"
	
	def __repr__(self):
		return f"ParentNode({self.tag}, {self.children}, {self.props})"