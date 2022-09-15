def bestdeal_sorting(data, price_range, distance_range):
    sorted_list = list()

    min_price, max_price = map(int, price_range.split("-"))
    min_dist, max_dist = map(int,  distance_range.split("-"))

    for i_hotel in data:
        if "ratePlan" in i_hotel.keys() and "landmarks" in i_hotel.keys():
            i_distance, _ = i_hotel["landmarks"][0]["distance"].split(" ")
            i_price = int(i_hotel["ratePlan"]["price"]["exactCurrent"])
            i_distance = i_distance.replace(",", ".")
            if min_price <= i_price <= max_price and min_dist <= float(i_distance) <= max_dist:
                sorted_list.append(i_hotel)
    return sorted_list
