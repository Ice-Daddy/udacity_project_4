
from PIL import Image
from urllib2 import urlopen


class Pixelator():

    def __download(self, url):
        self.image = Image.open(urlopen(url))

    def __open(self, file_path):
        self.image = Image.open(file_path)

    def __calculate_factor(self):
        max_pixel = max(self.image.size)
        return max_pixel // 100

    def __pixelate(self, output_path):
        height, width = self.image.size
        factor = self.__calculate_factor()
        self.image = self.image.resize(
            (height // factor, width // factor),
            Image.NEAREST
        )
#       self.image = self.image.resize(
#           (height * factor, width * factor),
#           Image.NEAREST
#       )
        self.image.save(output_path)

    def pixelate_locally(self, input_path, output_path):
        self.__open(input_path)
        self.__pixelate(output_path)

    def pixelate_url(self, url, output_path):
        self.__download(url)
        self.__pixelate(output_path)


if __name__ == '__main__':
    inventory = [
        (
            "https://free.clipartof.com/1729-Free-Clipart-Of-A-Pair-Of-Mens-Shoes.png",
            "feet/default.png"
        ),
        (
            "https://static1.squarespace.com/static/527ab762e4b0495cc4f23725/52c5cebde4b068c3c20aa599/52c5cf45e4b0e8cd7198afce/1388695367041/Ari.png?format=500w",
            "torso/default.png"
        ),
        (
            "https://cdn2.iconfinder.com/data/icons/spiritual-line-3/512/witch_hat_wizard_magic-512.png",
            "head/default.png"
        ),
        (
            "http://www.clker.com/cliparts/A/u/X/C/V/3/gloves-outline-md.png",
            "hands/default.png"
        ),
        (
            "http://clipart.coolclips.com/480/vectors/tf05273/CoolClips_vc048815.png",
            "right-hand/default.png"
        ),
        (
            "http://origin.webcdn.theblackdesertonline.net/forum/service_live/monthly_12_2015/pikachu.png.004fd8ca0febcb09f8897aecbe1692b0.png",
            "companion/default.png"
        ),
        (
            "https://www.denhamthejeanmaker.com/on/demandware.static/-/Library-Sites-Global/default/dwe56105cb/images/fits/512/Razor-Front.png",
            "legs/default.png"
        ),
        (
            "https://cdn1.iconfinder.com/data/icons/arms-and-armor-outlines/300/18-512.png",
            "left-hand/default.png"
        ),
        (
            "http://www.medievalarmour.com/images/Product/large/MY100611.png",
            "head/viking_helmet.png"
        ),
        (
            "http://www.medievalarmour.com/images/Product/large/AH-6792.png",
            "head/medieval_helmet.png"
        ),
        (
            "https://www.swordsofmight.com/wp-content/uploads/2016/05/Warriors-Leather-Helmet-Side-600x600.png",
            "head/simple_leather_helmet.png"
        ),
        (
            "https://cdn.shopify.com/s/files/1/1819/9163/products/death-metal-rainbow-cute-shirts-t-shirt-gildan-womens-t-shirt-purple-s-teeqq-11_1000x.png?v=1505259192",
            "torso/metal_shirt.png"
        ),
        (
            "http://www.clker.com/cliparts/C/H/o/A/i/k/pink-shirt-hi.png",
            "torso/pink_t-shirt.png"
        ),
        (
            "http://www.regencyaesthetics.co.uk/wp-content/uploads/2017/03/excessive-sweating-transparent.png",
            "torso/sweat_soaked_shirt.png"
        ),
        (
            "https://vignette.wikia.nocookie.net/runescape2/images/2/2e/Studded_chaps_detail.png/revision/latest?cb=20120220184458",
            "legs/leather_punk_pants.png"
        ),
        (
            "https://cdn.pcpclothing.com/wp-content/uploads/20161213061844/red-glitter-03.png",
            "legs/groovy_glittery_pants.png"
        ),
        (
            "https://static.trendme.net/temp/thumbs/280-420-2-90/ripped-jeans_Capri---Cropped-liekeotter-full-10704-563392.png",
            "legs/ripped_jeans.png"
        ),
        (
            "http://www.faizansafety.com/images/large/207.png",
            "hands/hand_knit_gloves.png"
        ),
        (
            "https://cdn.shopify.com/s/files/1/0509/3401/products/Cutters1_b9e13e4f-c0f5-40cd-931a-28cb78d94f77.png?v=1501176651",
            "hands/red_gloves.png"
        ),
        (
            "https://i.ebayimg.com/images/g/FfwAAOSwf15aVjD-/s-l300.png",
            "hands/metal_gloves.png"
        ),
        (
            "https://cdn.pixabay.com/photo/2014/03/25/16/27/tennis-shoes-297150_960_720.png",
            "feet/tennis_shoes.png"
        ),
        (
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAaRDh5S_sMTAty6Mmb-hwFfLfpZLyzxC1YaEphTlMCC_6QaQfBQ",
            "feet/scooberdiver_shoes.png"
        ),
        (
            "https://i.pinimg.com/originals/16/52/4a/16524a1d9a2d5bc00a2644dcd4562229.jpg",
            "feet/running_shoes.png"
        ),
        (
            "https://i1.wp.com/besttorquewrenches.com/wp-content/uploads/2015/11/screwdriver-29367_640.png",
            "left-hand/screwdriver.png"
        ),
        (
            "https://png.icons8.com/metro/1600/spade.png",
            "left-hand/spade.png"
        ),
        (
            "http://www.groz-tools.com/india/Pix/Handyman's-Hacksaw,-CB-46.png",
            "left-hand/hacksaw.png"
        ),
        (
            "http://www.cmusic.pro/wp-content/uploads/2017/11/t-trombone.png",
            "right-hand/trombone.png"
        ),
        (
            "https://vignette.wikia.nocookie.net/scribblenauts/images/6/6f/Triangle_Instrument.png/revision/latest?cb=20130408222701",
            "right-hand/triangle.png"
        ),
        (
            "https://vignette.wikia.nocookie.net/pocoyoworld/images/e/e1/Tambourine.gif/revision/latest?cb=20131203034410",
            "right-hand/tambourine.png"
        ),
        (
            "http://origin.webcdn.theblackdesertonline.net/forum/service_live/monthly_12_2015/pikachu.png.004fd8ca0febcb09f8897aecbe1692b0.png",
            "companion/pikachu.png"
        ),
        (
            "http://static.pokemonpets.com/images/monsters-images-300-300/26-Raichu.png",
            "companion/raichu.png"
        ),
        (
            "https://i1.wp.com/pokemongoden.com/wp-content/uploads/2016/07/Charmander-Pokedex.png?fit=250%2C282",
            "companion/charmander.png"
        )
    ]
    px = Pixelator()
    loc = '/home/moritz/Desktop/Programming/udacity/git/pkg/static/img/'
    for url, path in inventory:
        try:
            px.pixelate_url(url, loc + path)
        except:
            print("skipped one image")

