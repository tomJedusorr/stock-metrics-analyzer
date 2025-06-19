def tick_to_str(tick_str):

    if isinstance(tick_str, list):
        list_adj = tick_str
    else:
        list_tick = []
        list_tick.append(tick_str)

        # When no information found, the function returns "-1"
        if list_tick[0].find(",") > -1:

            list_adj = list_tick[0].replace(" ", "").split(",")

        elif list_tick[0].find(";") > -1:

            list_adj = list_tick[0].replace(" ", "").split(";")
        
        else:
            list_adj = list_tick

    return list_adj