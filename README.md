Installation:

You guessed it...

```python
pip install assetman

```

The simplest incarnation of this library goes as follows:

```python
import assetman

assetman.configure(aws_key, aws_secret, my_bucket)
some_data = 'my awsome string / image binary / html / markdown / national secrets'
asset = assetman.create_asset(some_data)
asset.public = True # makes the asset publicly accessible over S3
assetman.save_asset(asset)

print asset.uuid # returns a 16 character UUID which you can save for later

# then later

my_saved_asset = assetman.get_asset(uuid)

print my_saved_asset.data
'my awsome string / image binary / html / markdown / national secrets'
```

It is also important to note that there are some convenience Asset Types built in for convenient handling
of meta data and mimetypes.

For example, the Image asset type will track format and dimensions for you.

Here is an example from the test suite that uses Wand, which is a pretty sweet little library by the way. Rock on, South Korea.

```python
from wand.image import Image
import assetman

with Image(filename=path.join(path.dirname(__file__), 'fixtures/faceoff.jpg')) as image:
		assetman.configure(test_key, test_secret, test_bucket)
		asset = assetman.create_image(image.make_blob(), image.height, image.width, image.mimetype)
		uuid = assetman.save_asset(asset)
		saved_image = assetman.get_asset(uuid)
		assert_equal(long(saved_image.height), image.height)
		assert_equal(long(saved_image.width), image.width)
		assert_equal(saved_image.mime_type, image.mimetype)
```

Basically the convience types just provide shortcutting for the meta data to be saved and retrieved.

Enjoy! More convenience types / methods appreciated.

Testing

The tests are supposed to be run with nose. Wand is an optional dependency that is not included by default
but will need to be in order to run the tests for the image suite. It is recommended that you install it.

```python
nosetests assetman/tests

```