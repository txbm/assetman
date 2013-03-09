import assetman
from nose.tools.trivial import assert_is_instance, assert_equal

test_key = u'AKIAIV2YPEVVWTOK4I7A'
test_secret = u'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'
test_bucket = u'gsci-test'

def test_get_manager():
	manager = assetman.get_manager(test_key, test_secret, test_bucket)
	assert_is_instance(manager, assetman.model.AssetMan)

def test_configure():
	assetman.configure(test_key, test_secret, test_bucket)
	assert_is_instance(assetman.manager, assetman.model.AssetMan)
	assetman.manager = None

def test_create_asset():
	data = 'herpidius derpidius'
	assetman.configure(test_key, test_secret, test_bucket)
	asset = assetman.create_asset(data)
	assert_is_instance(asset, assetman.model.Asset)
	del asset
	assetman.manager = None

def test_save_asset():
	data = 'marcus aurelius'
	assetman.configure(test_key, test_secret, test_bucket)
	asset = assetman.create_asset(data)
	assetman.save_asset(asset)
	del asset
	assetman.manager = None

def test_get_asset():
	data = 'julius caesar'
	assetman.configure(test_key, test_secret, test_bucket)
	asset = assetman.create_asset(data)
	assetman.save_asset(asset)
	uuid = asset.uuid
	del asset
	asset = assetman.get_asset(uuid)
	assert_is_instance(asset, assetman.model.Asset)
	assert_equal(asset.data, data)
	assetman.manager = None