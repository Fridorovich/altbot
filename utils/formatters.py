from config import STATA_FORMAT

def get_populations_formatted(world_totals, main_data):
    pop_ss_percent = (main_data[4] / world_totals[1] * 100) if main_data[4] else 0
    pop_ns_percent = (main_data[5] / world_totals[2] * 100) if main_data[5] else 0
    pop_nns_percent = (main_data[6] / world_totals[3] * 100) if main_data[6] else 0
    pop_nnns_percent = (main_data[7] / world_totals[4] * 100) if main_data[7] else 0

    return (
        f"{main_data[4]:,} (СС, {round(pop_ss_percent, 2)}% от населения СС), " if pop_ss_percent else "",
        f"{main_data[5]:,} (НС, {round(pop_ns_percent, 2)}% от населения НС), " if pop_ns_percent else "",
        f"{main_data[6]:,} (ННС, {round(pop_nns_percent, 2)}% от населения ННС), " if pop_nns_percent else "",
        f"{main_data[7]:,} (НННС, {round(pop_nnns_percent, 2)}% от населения НННС), " if pop_nnns_percent else "",
        round(sum(filter(None, main_data[4:8])) / sum(filter(None, world_totals[1:])) * 100, 2),
        f"{round(main_data[8], 2)}% (СС), " if main_data[8] else "",
        f"{round(main_data[9], 2)}% (НС), " if main_data[9] else "",
        f"{round(main_data[10], 2)}% (ННС), " if main_data[10] else "",
        f"{round(main_data[11], 2)}% (НННС), " if main_data[11] else "",
    )

def format_stata(world_totals, main_data):
    return STATA_FORMAT.format(
        main_data[0],
        main_data[1],
        main_data[2],
        main_data[3],
        round(main_data[3] / world_totals[0] * 100, 2),
        *get_populations_formatted(world_totals, main_data),
        main_data[12],
        main_data[13],
        main_data[14],
        main_data[15],
        main_data[16],
        main_data[12] - main_data[13]
    )