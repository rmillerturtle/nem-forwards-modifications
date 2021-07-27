import numpy as np
import pandas as pd
import copy
import util
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    percentle_replace = 0.80

    LGC_CURVE_PRICE_FLOOR = {2022:-38.6,2023:-18.7,2024:-15.2,2025:-15.8,2026:-15.7,2027:-15.9,2028:-11.4,2029:-8.0,2030:-2.7}

    SA_PRICE_FLOOR = {2022:-1000,2023:-1000,2024:-1000,2025:-15.8,2026:-15.7,2027:-15.9,2028:-11.4,2029:-8.0,2030:-2.7}

    cur = util.get_snowflake_conector()
    snowflake_table = "snwflk_TRADINGPRICE"
    snowflake_market = "RRP"
    region = "VIC"
    historical_data_start_date = datetime.datetime(year=2020,month=7,day=1,hour=0, minute=30,second=0)
    historical_data_end_date = datetime.datetime(year=2021,month=7,day=2,hour=0, minute=0,second=0) #extra day so leap years are easy

    ref_year_prices = util.get_snowflake_historical_price_curves(cur, snowflake_table, snowflake_market, region_id=region,
                                                         start_date=historical_data_start_date, end_date=historical_data_end_date)

    sorted_ref_year_prices = ref_year_prices.sort_values(by=['RRP'], ascending=False, ignore_index=True)
    sorted_ref_year_prices.index.name = 'index'
    sorted_ref_year_prices['PERCENTILE'] = sorted_ref_year_prices.index * (1 / len(sorted_ref_year_prices.index))
    snowflake_market = "RRP"
    snowflake_table = "FORWARD_CURVES"
    forwards_version = "CORNWALL_2021"


    year_index = 2022
    while year_index < 2023:
        cur = util.get_snowflake_conector()
        forward_data_start_date = datetime.datetime(year=year_index, month=1, day=1, hour=0, minute=30, second=0)
        forward_data_end_date = datetime.datetime(year=year_index+1, month=1, day=1, hour=0, minute=0, second=0)
        forward_energy_prices = util.get_snowflake_forward_price_curves(cur, snowflake_table, snowflake_market,
                                                                        region_id=region,
                                                                        start_date=forward_data_start_date,
                                                                        end_date=forward_data_end_date,
                                                                        forwards_version=forwards_version)

        forward_energy_prices['SETTLEMENTDATE'] = forward_energy_prices['SETTLEMENTDATE'] + pd.Timedelta(hours=10)
        forward_energy_prices['Year'] = forward_energy_prices['SETTLEMENTDATE'].dt.year
        sorted_forward_energy_prices = forward_energy_prices.sort_values(by=['RRP'], ascending=False, ignore_index=True)
        sorted_forward_energy_prices.index.name = 'index'
        sorted_forward_energy_prices['PERCENTILE'] = sorted_forward_energy_prices.index * (1 / len(sorted_forward_energy_prices.index))
        print(sorted_forward_energy_prices)

        # print(sorted_ref_year_prices)
        #
        # if year_index < 2031:
        #     economic_price_floor = SA_PRICE_FLOOR[year_index]
        # else:
        #     economic_price_floor = 0
        #
        # for i in sorted_forward_energy_prices.index.values:
        #     if sorted_forward_energy_prices.loc[i,'PERCENTILE'] > percentle_replace and sorted_forward_energy_prices.loc[i,'RRP'] > sorted_ref_year_prices.loc[i, 'RRP']:
        #        sorted_forward_energy_prices.loc[i, 'RRP'] = max(sorted_ref_year_prices.loc[i, 'RRP'],economic_price_floor)
        #
        #
        # resorted_forward_energy_prices = sorted_forward_energy_prices.sort_values(by=['SETTLEMENTDATE'], ascending=True, ignore_index=True)
        # resorted_forward_energy_prices = resorted_forward_energy_prices.drop(columns=['Year', 'PERCENTILE'])
        #
        # if year_index == 2022:
        #     final_prices_modified = resorted_forward_energy_prices
        #
        # else:
        #     final_prices_modified = final_prices_modified.append(resorted_forward_energy_prices,ignore_index = True)
        # print(resorted_forward_energy_prices)

        year_index = year_index + 5


    #final_prices_modified.to_csv(region + '_FDV1.csv', index=False)

    ax = sns.lineplot(data=sorted_ref_year_prices.iloc[20:], x = 'PERCENTILE' ,y="RRP")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.05))
    ax = sns.lineplot(data=sorted_forward_energy_prices.iloc[20:], x = 'PERCENTILE' ,y="RRP")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.05))
    ax.legend(['Historical Jul 2020 to July 2021','Cornwall Modified V1 2022'])
    plt.show()


