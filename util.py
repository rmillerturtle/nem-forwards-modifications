import snowflake.connector
import os

def get_snowflake_conector():

    conn = snowflake.connector.connect(
        user= os.environ.get("snowflakeUsername"),
        password= os.environ.get("snowflakePassword"),
        account="ke74435",
        warehouse="REVFORECAST_WH",
        database="AMS_MASTER",
    )

    cur = conn.cursor()
    return cur


def get_snowflake_forward_price_curves(cur, snowflake_table,snowflake_market, region_id, start_date, end_date,forwards_version):

    start_date = start_date.strftime("%Y-%m-%d %H:%M:%S") + '.000000000 +10:00'
    end_date = end_date.strftime("%Y-%m-%d %H:%M:%S") + '.000000000 +10:00'

    market = snowflake_market
    MYTABLE =  snowflake_table
    start_date_snwflk = "'" + start_date + "'"
    end_date_snwflk = "'" + end_date + "'"
    region_id_snwflk = "'" + region_id + "1'"
    VERSION = "'" + forwards_version + "'"
    sql = f'SELECT settlementdate, {market} FROM "{MYTABLE}" where settlementdate between {start_date_snwflk} and {end_date_snwflk} and REGIONID = {region_id_snwflk} and VERSION = {VERSION} order by settlementdate'
    cur.execute(sql)

    # Fetch the result set from the cursor and deliver it as the Pandas DataFrame.
    prices = cur.fetch_pandas_all()

    return prices

def get_snowflake_historical_price_curves(cur, snowflake_table,snowflake_market, region_id, start_date, end_date):

    start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
    end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

    market = snowflake_market
    MYTABLE =  snowflake_table
    start_date_snwflk = "'" + start_date + "'"
    end_date_snwflk = "'" + end_date + "'"
    region_id_snwflk = "'" + region_id + "1'"
    sql = f'SELECT settlementdate, {market} FROM "{MYTABLE}" where settlementdate between {start_date_snwflk} and {end_date_snwflk} and REGIONID = {region_id_snwflk}  order by settlementdate'
    cur.execute(sql)

    # Fetch the result set from the cursor and deliver it as the Pandas DataFrame.
    prices = cur.fetch_pandas_all()

    return prices

