def make_image_url(id, actual_json, for_variant):
    images_to_return_for_variant = []
    images_to_return = ["NO IMAGE AVAILABLE", "NO IMAGE AVAILABLE", "NO IMAGE AVAILABLE"]
    images_dict = actual_json["[data-role=swatch-options]"]["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]["images"][str(id)]
    position_count = len(images_dict)
    if position_count == 1:
        image = images_dict[0]["full"]
        position = images_dict[0]["position"]
        if for_variant and position == "1":
            images_to_return_for_variant.append(image)
            return images_to_return_for_variant
        elif for_variant and position != "1":
            images_to_return_for_variant.append("NO IMAGE AVAILABLE")
            return images_to_return_for_variant
        elif not for_variant:
            if position == "1":
                images_to_return[0] = image
            elif position_count == "2":
                images_to_return[1] = image
            elif position_count == "3":
                images_to_return[2] = image
            return images_to_return              

    elif position_count == 3:
        if for_variant:
            for each_image in images_dict:
                image = each_image["full"]
                position = each_image["position"]
                if position == "1":
                    images_to_return_for_variant.append(image)
                    break
            return images_to_return_for_variant
        else:
            for each_image in images_dict:
                image = each_image["full"]
                position = each_image["position"]
                if position == "1":
                    images_to_return[0] = image
                elif position_count == "2":
                    images_to_return[1] = image
                elif position_count == "3":
                    images_to_return[2] = image
            return images_to_return
    else:
        if for_variant:
            for each_image in images_dict:
                image = each_image["full"]
                position = each_image["position"]
                if position == "1":
                    images_to_return_for_variant.append(image)
            if not images_to_return_for_variant:
                images_to_return_for_variant.append("NO IMAGE AVAILABLE")
            return images_to_return_for_variant
        else:
            for each_image in images_dict:
                image = each_image["full"]
                position = each_image["position"]
                if position == "1":
                    images_to_return[0] = image
                elif position_count == "2":
                    images_to_return[1] = image
                elif position_count == "3":
                    images_to_return[2] = image
            return images_to_return



                
            
            




