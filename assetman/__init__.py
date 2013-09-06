from .model import AssetMan, Asset

manager = None

def get_manager(key, secret, bucket):
	return model.AssetMan(key, secret, bucket)

def configure(key, secret, bucket):
	global manager
	if not manager:
		manager = get_manager(key, secret, bucket)

def create_asset(data):
	return model.Asset(data)

def create_image(data, height, width, mimetype):
	return model.Image(data, height, width, mimetype)

def save_asset(asset):
	if not manager:
		raise model.NotConfigured()
	return manager.save_asset(asset)

def get_asset(uuid):
	if not manager:
		raise model.NotConfigured()
	return manager.get_asset(uuid)

def delete_asset(uuid):
	if not manager:
		raise model.NotConfigured()
	return manager.delete_asset(uuid)