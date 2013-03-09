import uuid
import s3ops

mime_type_asset_map = {}

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

	def get_asset(self, uuid):
		connection = self.connect()
		bucket = s3ops.get_bucket(self.bucket_name, connection)
		key = s3ops.get_key(bucket, uuid)
		asset = Asset(key.get_contents_as_string())
		acl = key.get_acl()
		asset.url = key.generate_url(120)
		asset.mime_type = key.content_type
		asset.meta_data = key.metadata
		return asset

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
		return self.__class__.__name__.lower()

class Image(Asset):

	def __init__(self, data, height, width, mimetype):
		super(self, Image).__init__(data)
		self.meta_data['height'] = height
		self.meta_data['width'] = width
		self.mime_type = mimetype

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