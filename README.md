LiveCC.py
==============

Record English speech and translate it to Spanish text.

This script is a combination of two scripts (see Credit section below) that allows you to record your English speech through your PC Mic and have it translated and displayed to the screen in Spanish. Thus giving you a live closed caption of your presentation. 

Enjoy!


Registering your application
----------------------------

In order to use the Bing translate API you must first register your application and update the
`translator = Translator('<Your Client ID>', '<Your Client Secret>')`
line in `livecc.py`

To register your application with Azure DataMarket, visit https://datamarket.azure.com/developer/applications/. 

>If you do not yet have a developer account or haven't yet signed up for Bing Translate go here first: [https://datamarket.azure.com/dataset/1899a118-d202-492c-aa16-ba21c33c06cb](https://datamarket.azure.com/dataset/1899a118-d202-492c-aa16-ba21c33c06cb). 

Click on “Register”. In the
“Register your application” dialog box, you can define your own
Client ID and Name. The redirect URI is not used for the Microsoft
Translator API. However, the redirect URI field is a mandatory field,
and you must provide a URI to obtain the access code. A description is
optional.

Contributing
------------

Feel free to fork and send [pull requests](http://help.github.com/fork-a-repo/).  Contributions welcome.

Credit
------------

[python-google-speech-scripts](https://github.com/jeysonmc/python-google-speech-scripts)

[Microsoft-Translator-Python-API](https://github.com/openlabs/Microsoft-Translator-Python-API)

License
-------

python-google-speech-scripts is released under the [MIT](http://opensource.org/licenses/MIT) LICENSE.

Microsoft-Translator-Python-API is released under the [Openlabs](https://github.com/openlabs/Microsoft-Translator-Python-API/blob/master/LICENSE) LICENSE.
