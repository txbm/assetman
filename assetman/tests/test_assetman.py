# -*- coding: utf-8 -*-

from nose.tools.trivial import assert_is_instance, assert_equal
from os import path
from wand.image import Image

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
	assetman.manager = None

def test_save_asset():
	data = 'marcus aurelius'
	assetman.configure(test_key, test_secret, test_bucket)
	asset = assetman.create_asset(data)
	uuid = assetman.save_asset(asset)
	assetman.delete_asset(uuid)
	assetman.manager = None

def test_get_asset():
	data = 'julius caesar'
	assetman.configure(test_key, test_secret, test_bucket)
	asset = assetman.create_asset(data)
	uuid = assetman.save_asset(asset)
	asset = assetman.get_asset(uuid)
	assert_is_instance(asset, assetman.model.Asset)
	assert_equal(asset.data, data)
	assetman.delete_asset(uuid)
	assetman.manager = None

def test_create_image():
	with Image(filename=path.join(path.dirname(__file__), 'fixtures/faceoff.jpg')) as image:
		assetman.configure(test_key, test_secret, test_bucket)
		asset = assetman.create_image(image.make_blob(), image.height, image.width, image.mimetype)
		uuid = assetman.save_asset(asset)
		saved_image = assetman.get_asset(uuid)
		assert_equal(long(saved_image.height), image.height)
		assert_equal(long(saved_image.width), image.width)
		assert_equal(saved_image.mime_type, image.mimetype)
	assetman.delete_asset(uuid)
	assetman.manager = None