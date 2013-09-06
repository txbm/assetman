import uuid

from boto.s3.connection import S3Connection

mime_type_asset_map = {}

class Manager(object):

	def __init__(self, ctx_pool=1, rr=True, split_size=None, public=True):
		self._ctx_pool = ctx_pool
		self._rr = rr
		self._split_size = split_size
		self._public = public

	def authorize(self, key, secret):
		self._key = key
		self._secret = secret

	def new_asset(self, data):

class Connection(object):

	def __init__(self, key, secret):
		self._key = key
		self._secret = secret

	def _connect(self):
		if self._connection is not None:
			self._connection = 


	def upload(self, data, **kwargs):




class AssetMan(object):
	aws_key = None
	aws_secret = None
	bucket_name = None
	_connection = None

	def __init__(self, key, secret, bucket):
		self.aws_key = key
		self.aws_secret = secret
		self.bucket_name = bucket

	def connect(self):
		if not self._connection:
			self._connection = s3ops.get_connection(self.aws_key, self.aws_secret)
		return self._connection

	def save_asset(self, asset):
		connection = self.connect()
		bucket = s3ops.get_bucket(self.bucket_name, connection)
		asset.generate_uuid()
		s3ops.upload_string_data(bucket, asset.uuid, asset.data, asset.public, asset.mime_type, asset.meta_data)
		return asset.uuid # just some api fluidics

	def get_asset(self, uuid):
		connection = self.connect()
		bucket = s3ops.get_bucket(self.bucket_name, connection)
		key = s3ops.get_key(bucket, uuid)
		asset_type = key.get_metadata('asset_type')
		if asset_type == 'image':
			asset = Image(key.get_contents_as_string())
		else:
			asset = Asset(key.get_contents_as_string())
		acl = key.get_acl()
		asset.url = key.generate_url(120)
		asset.mime_type = key.content_type
		asset.meta_data = key.metadata
		return asset

	def delete_asset(self, uuid):
		connection = self.connect()
		bucket = s3ops.get_bucket(self.bucket_name, connection)
		s3ops.delete_key(bucket, uuid)

class Asset(object):
	mime_type = None
	meta_data = {}
	public = False
	uuid = None

	def __init__(self, data=None):
		self.data = data

	def generate_uuid(self):
		if not self.uuid:
			self.uuid = uuid.uuid4()

	@property
	def type(self):
		return self.meta_data['asset_type']

class Image(Asset):

	def __init__(self, data, height=None, width=None, mimetype=None):
		super(Image, self).__init__(data)
		if height:
			self.meta_data['height'] = height
		if width:
			self.meta_data['width'] = width
		if mimetype:
			self.mime_type = mimetype
		self.meta_data['asset_type'] = 'image'

	@property
	def height(self):
		return self.meta_data['height']

	@property
	def width(self):
		return self.meta_data['width']


class AssetManException(Exception): pass

class NotConfigured(AssetManException):

	def __str__(self):
		return 'You cannot make calls to read or write asset data until you have called the configure() method with your S3 information.'