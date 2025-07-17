# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
# wtite up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = int(getenv("API_ID", "24122570"))
API_HASH = getenv("API_HASH", "33bbfdf4cbc5dedc27257d1d3934e42a")
BOT_TOKEN = getenv("BOT_TOKEN", "7534544400:AAFxSHyQHA9631DC_kI_sM2Dbdj2AquJaZ8")
OWNER_ID = list(map(int, getenv("OWNER_ID", "8181241262").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://sujoy123m:wTWKGUaxYE7dxb1l@cluster0.zorxb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = getenv("LOG_GROUP", "-1002789128451")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1001965166816"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "1000"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500000"))
WEBSITE_URL = getenv("WEBSITE_URL", "upshrink.com")
AD_API = getenv("AD_API", "52b4a2cf4687d81e7d3f8f2b7bc2943f618e78cb")
STRING = getenv("STRING", "BQEKjbEAtQhq7FYVGrBkaa4_YG7Ywc2IUbWxxFOBGPgTeBk-xtgy2l2vZn9Ago7l4LyRIPSkl4hgSqFixEX6W0AbgpwIGX1EeeCxRu1rFFjzd_J2zH-eyHKp-JOQdEBKRNIosloxMwm4ge7cx3T25B2kDW7v3RIhcpwJk2yGrD74scEC17e4Z-95TNnHfzaXOeT6brdeba5J_gPlkOS4KRaD89QP3ow_MbR_Z8mI28SSzJN-tc09brNX7vhq0dDx-x5Ahn60SAtxWJUqwZZyOvcQD7f1gDH4uoJhjepNLP-KcK6H2oqxpU7PpCrujCbwu1E4NaOI9kgFUHTpHxZMwJG9xPk83gAAAAGmklF5AA")
YT_COOKIES = getenv("YT_COOKIES", YTUB_COOKIES)
DEFAULT_SESSION = getenv("DEFAUL_SESSION", "BQEKjbEAtQhq7FYVGrBkaa4_YG7Ywc2IUbWxxFOBGPgTeBk-xtgy2l2vZn9Ago7l4LyRIPSkl4hgSqFixEX6W0AbgpwIGX1EeeCxRu1rFFjzd_J2zH-eyHKp-JOQdEBKRNIosloxMwm4ge7cx3T25B2kDW7v3RIhcpwJk2yGrD74scEC17e4Z-95TNnHfzaXOeT6brdeba5J_gPlkOS4KRaD89QP3ow_MbR_Z8mI28SSzJN-tc09brNX7vhq0dDx-x5Ahn60SAtxWJUqwZZyOvcQD7f1gDH4uoJhjepNLP-KcK6H2oqxpU7PpCrujCbwu1E4NaOI9kgFUHTpHxZMwJG9xPk83gAAAAGmklF5AA")  # added old method of invite link joining
INSTA_COOKIES = getenv("INSTA_COOKIES", INST_COOKIES)
