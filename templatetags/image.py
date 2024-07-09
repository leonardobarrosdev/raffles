from django import template

register = template.Library()

@register.filter
def get_image(h, key):
	''' Receive a dictionary with product id and image
	return a url image
	'''
	try:
		img_url = h[key].image.url
	except:
		img_url = None
	return img_url
