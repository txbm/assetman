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

Here is an example using Wand, which is a pretty sweet little library by the way. Go South Korea!

```python
import wand
import assetman

assetman.configure(aws_key, aws_secret, my_bucket)

# assume read in some_binary_image from file

with wand.image.Image(blob=some_binary_image) as image:
	asset = assetman.create_image(image, image.height, image.width, image.mimetype)
	uuid = assetman.save_asset(asset)

saved_image = assetman.get_asset(uuid)
print saved_image.height # will print the height
print saved_image.width # will print the width
print saved_image.format # and the format
print saved_image.mime_type # will print the proper mime type
```

Basically the convience types just provide shortcutting for the meta data to be saved and retrieved.

Enjoy! More convenience types / methods appreciated.

Testing

The tests are supposed to be run with nose. Wand is an optional dependency that is not included by default
but will need to be in order to run the tests for the image suite. It is recommended that you install it.

```python

nosetests assetman/tests

```