import re


class Highlighter():

	def __init__(self, text_buffer):
		self.syntax = []
		self.text_buffer = text_buffer

	def get_content(self):

		start_iter = self.text_buffer.get_start_iter()
		end_iter = self.text_buffer.get_end_iter()
		return self.text_buffer.get_text(start_iter, end_iter, True)

	def clear(self):
		start = self.text_buffer.get_start_iter()
		end = self.text_buffer.get_end_iter()
		self.text_buffer.remove_all_tags(start, end)

	def perform(self):
		self.clear()
		for regexp_object_list, tag in self.syntax:
			self.highlight(regexp_object_list, tag)

	# create from list of keywords
	def add_words(self, syntax_list, tag_name, **tag_keyed_parameters):

		regexp_object_list = []
		for statement in syntax_list:
			regexp_object_list += [re.compile("(^|[,\s=(])(?P<highlight>" + statement + ")($|[:\s(),]+?)", re.M)]
		self.add(regexp_object_list, tag_name, **tag_keyed_parameters)

	def add(self, regexp_list, tag_name, **tag_keyed_parameters):

		tag = self.text_buffer.create_tag(tag_name, **tag_keyed_parameters)
		self.syntax += [[regexp_list, tag]]

	def highlight(self, regexp_object_list, tag):
		for regexp_object in regexp_object_list:
			for match in regexp_object.finditer(self.get_content()):
				if "highlight" in match.groupdict():
					start = match.start("highlight")
					end = match.end("highlight")
				else:
					start = match.start()
					end = match.end()
				start_iter = self.text_buffer.get_iter_at_offset(start)
				end_iter = self.text_buffer.get_iter_at_offset(end)
				self.text_buffer.apply_tag(tag, start_iter, end_iter)

