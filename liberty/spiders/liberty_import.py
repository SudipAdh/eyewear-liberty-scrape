import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import json
from ..formatting_methods import make_image_url

class Spidey(scrapy.Spider):

    name = "liberty"
    # for youth
    youth_urls = [
        "https://www.libertysport.com/youth/sport-protective.html?product_list_limit=36",
        "https://www.libertysport.com/youth/everyday-ophthalmic.html",
        "https://www.libertysport.com/youth/swim-goggles.html",
        "https://www.libertysport.com/adult/sport-protective.html?product_list_limit=36",
        "https://www.libertysport.com/adult/everyday-ophthalmic.html",
        "https://www.libertysport.com/adult/swim-goggles.html",
        "https://www.libertysport.com/adult/ppe.html",
        "https://www.libertysport.com/adult/performance-sunglasses.html",
        "https://www.libertysport.com/adult/switch-interchange.html",
        "https://www.libertysport.com/adult/motorcycle.html",

    ]
    start_urls = youth_urls

    def parse(self, response):
        if "sport-protective" in response.url:
            type_ = "Sunglasses"
        elif "everyday-ophthalmic" in response.url:
            type_ = "Eyeglasses"
        elif "swim-goggles" in response.url:
            type_ = "Goggles"
        elif "ppe" in response.url:
            type_ ="Ppe"
        elif "sunglasses" in response.url:
            type_ = "Sunglasses"
        elif "switch-interchange" in response.url:
            type_ = "Switch Interchange"
        elif "motorcycle" in response.url:
            type_ = "Motorcycle"
        product_urls = response.xpath("//a[contains(@class, 'product-item-link')]/@href").extract()
        for each_product in product_urls:
            # each_product = "https://www.libertysport.com/x8-200.html"
            yield scrapy.Request(each_product, callback=self.parse_products, cb_kwargs={"type":type_})
    
    def parse_products(self, response, **kwargs):
        data = dict()
        type_ = kwargs["type"]
        title =  response.xpath("//h1[contains(@class, 'page-title')]/span/text()").get().lower()
        handle = title.replace(" ", "-")
        price = response.xpath("//meta[contains(@property, 'product:price:amount')]/@content").get()
        body_html = response.xpath("//meta[contains(@name, 'description')]/@content").get()
        shape_ = "XXXXX"
        vendor = "Liberty"
        gender = "XXXXX"
        if "Unisex" in response.text:
            gender = "Unisex"
        gender_keywords = ["men", "women", "male", "female"]
        for each in gender_keywords:
            if each in body_html.lower():
                if each.startswith("m"):
                    gender = "Male"
                else:
                    gender = "Female"
                break
        lens_and_frames_datas = []
        variant_names = []
        json_data = response.xpath("//form[contains(@id, 'product_addtocart_form')]//script/text()").get().strip()
        actual_json = json.loads(json_data)
        lens_and_frames_names_id = actual_json["[data-role=swatch-options]"]["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]["attributes"]["139"]["options"]
        lens_and_frames_datas = []
        for each in lens_and_frames_names_id:
            temp_data = dict()
            temp_data["variant_name"] = each["label"]
            try:
                temp_data["id"] = each["products"][0]
            except Exception:
                continue
            lens_and_frames_datas.append(temp_data)
        tags = ""
        
        image_alts = []
        for each_variant in lens_and_frames_datas:
            variant_name = "["+each_variant["variant_name"].split("-")[0].strip()+"]"
            for _ in range(3):
                image_alts.append(variant_name)
        try:
            frames_t = ",".join(["Frame Color-"+each["variant_name"] for each in lens_and_frames_datas])
        except Exception:
            import pdb
            pdb.set_trace()
        
        try:
            lens_colors = ",".join([each["variant_name"].split("/")[-1] for each in lens_and_frames_datas if "/" in each["variant_name"]])
            lens_colors_t = ",".join(["Lens Color-"+each["variant_name"].split("/")[-1] for each in lens_and_frames_datas])
        except Exception:
            lens_colors = "Clear Lenses"
            lens_colors_t = "Clear Lenses"
        
        
        
        try:
            tags = ", ".join(["Category-"+type_, "Brand-"+vendor, "Price-"+str(price), "Gender-"+gender, "Shape-"+shape_,  frames_t, lens_colors_t])
            trade_symbols = re.findall(u'(\N{COPYRIGHT SIGN}|\N{TRADE MARK SIGN}|\N{REGISTERED SIGN})', tags)
            for each in trade_symbols:
                tags = tags.replace(each, "")
        except Exception:
            import pdb
            pdb.set_trace()
    

        option_1_name = "Frame Color/Lens Color"
        published = True
        gift_card = False

        variant_grams = 0
        varaint_inventory_tracker = "shopify"
        varaint_inventory_policy = "continue"
        variant_fulfillment_service = "manual"
        variant_requires_shipping = True
        variant_taxable = True
        variant_weight_unit = "lb"

        variant_images = []
        for each in lens_and_frames_datas:
            images = make_image_url(each["id"], actual_json, for_variant=True)
            variant_images.extend(images)

        write_once = 0
        position_count = 1
        i = 0
        for each in lens_and_frames_datas:
            
            alt_text = each["variant_name"]
            sku = each["id"]
            images = make_image_url(each["id"], actual_json, for_variant=False)
            for each in images:
                if each == "NO IMAGE AVAILABLE":
                    del image_alts[i]
                    continue
                image_alts
                if write_once != 0:
                    # handle = None
                    option_1_name = None
                    title = None
                    body_html = None
                    vendor = None
                    type_ = None
                    tags = None
                    published = None
                    gift_card = None
                image_src = each
                try:
                    frame_color_web = lens_and_frames_datas[i]["variant_name"].strip()
                    variant_sku = lens_and_frames_datas[i]["id"]
                    variant_price = price
                    if not variant_price:
                        variant_price = 329
                    variant_image = variant_images[i]
                    i += 1
                except Exception:
                    frame_color_web = None
                    frame_color = None
                    variant_sku = None
                    variant_price = None
                    variant_image = None
                    variant_requires_shipping = None
                    variant_taxable = None
                
                if not variant_sku:
                    variant_grams = None
                    varaint_inventory_tracker = None
                    varaint_inventory_policy = None
                    variant_fulfillment_service = None
                    variant_weight_unit = None
                
                if body_html:
                    body_html = "<p>"+body_html+"</p>"

                write_once = 1
                data["Handle"] = "liberty-"+handle.lower()
                if title:
                    data["Title"] = "Liberty "+title.title()
                    if "goggle" in title.lower():
                        type_ = "Goggles"
                else:
                    data["Title"] = title
                data["Body (HTML)"] = body_html
                data["Vendor"] = vendor
                data["Type"] = type_
                data["Tags"] = tags
                data["Published"] = published
                data["Option1 Name"] = option_1_name
                data["Option1 Value"] = frame_color_web
                data["Option2 Name"] = None
                data["Option2 Value"] = None
                data["Option3 Name"] = None
                data["Option3 Value"] = None
                # data["Frame Color/Lens Color (FROM SHOPIFY)"] = None
                # data["Frame Color/Lens Color (FROM WEBSITE)"] = frame_color_web
                # data["Frame Color (FROM SHOPIFY)"] = None
                # data["Frame Color (FROM WEBSITE)"] = frame_color
                data["Variant SKU"] = variant_sku
                data["Variant Grams"] = variant_grams
                data["Variant Inventory Tracker"] = varaint_inventory_tracker
                data["Variant Inventory Policy"] = varaint_inventory_policy
                data["Variant Fulfillment Service"] = variant_fulfillment_service
                data["Variant Price"] = variant_price
                data["Variant Compare At Price"] = None
                data["Variant Requires Shipping"] = variant_requires_shipping
                data["Variant Taxable"] = variant_taxable
                data["Variant Barcode"] = None
                data["Image Src"] = image_src
                data["Image Position"] = position_count
                data["Image Alt Text"] = image_alts[position_count-1]
                data["Gift Card"] = gift_card
                data["SEO Title"] = None
                data["SEO Description"] = None
                data["Google Shopping / Google Product Category"] = None
                data["Google Shopping / Gender"] = None
                data["Google Shopping / Age Group"] = None
                data["Google Shopping / MPN"] = None
                data["Google Shopping / AdWords Grouping"] = None
                data["Google Shopping / AdWords Labels"] = None
                data["Google Shopping / Condition"] = None
                data["Google Shopping / Custom Product"] = None
                data["Google Shopping / Custom Label 0"] = None
                data["Google Shopping / Custom Label 1"] = None
                data["Google Shopping / Custom Label 2"] = None
                data["Google Shopping / Custom Label 3"] = None
                data["Google Shopping / Custom Label 4"] = None
                data["Variant Image"] = variant_image
                data["Variant Weight Unit"] = variant_weight_unit
                data["Variant Tax Code"] = None
                data["Cost per item"] = None
                data["A"] = None
                data["B"] = None
                data["Bridge"] = None
                data["ED"] = None
                data["Meta Description"] = None
                data["Meta Features"] = None
                data["Lens Color"] = None
                data["Frame Colo"] = None
                data["SKU"] = None
                data["Lifestyle"] = None
                data["Fit"] = None
                data["Category"] = None
                data["Gender"] = None
                data["Frame Material"] = None
                data["Shape"] = None
                data["Mount"] = None
                data["Polar/Non Polar"] = None
                data["Lens Material"] = None
                position_count += 1
                yield data
