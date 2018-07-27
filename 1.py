data.reset_index(drop=True,inplace=True)
    data["wkd"] = all_data.register_time.dt.weekday
    data =  data.merge(wkd_hour_df,on=["wkd","hour"],how = "left")
    data["day"] = data.register_time.dt.day
    data["month"] = data.register_time.dt.month
    data["day_in_year"] = data.register_time.dt.dayofyear
    data["days_spfest"] = data["register_time"].map(lambda x: (x - pd.to_datetime("2018-02-16")).days)
    X = data.drop(["register_time"],axis=1)
    if "prediction_pay_price" in X.columns:
        X = X.drop("prediction_pay_price",axis=1)
    X["price_per"] = (X["pay_price"]+0.1)/(X["pay_count"]+0.1)
    
    X["pvp_win_rate"] = (X.pvp_win_count + 0.1)/(X.pvp_lanch_count+0.1)
    X["pve_win_rate"] = (X.pve_win_count+0.1)/(X.pve_lanch_count+0.1)
    X["pvp_rate"] = (X.pvp_lanch_count+0.1)/(X.pve_lanch_count+0.1)
    X["pvp_vs_pve_win"] = (X.pvp_win_count+0.1)/(X.pve_win_count+0.1)
    gc.collect()
    X = X.merge(hour_mean,on="hour",how = "left")
    X = X.merge(wkd_mean,on="wkd",how="left")
    X = X.merge(dayinyear_mean,how="left",on="day_in_year")
    X = X.merge(dayinyear_hr_mean,how="left",on=["day_in_year","hour"])   
    X["avg_pay_price"] = X.pay_price/(X.avg_online_minutes+0.01)
    X["avg_pay_count"] = X.pay_count/(X.avg_online_minutes+0.01)
    X.loc[X.avg_online_minutes == 0,"avg_pay_price"] = 0
    X.loc[X.avg_online_minutes == 0,"avg_pay_count"] = 0
    X["build_remain"] = X.building_acceleration_add_value - X.building_acceleration_reduce_value
    X["build_use_rate"] = (X.building_acceleration_reduce_value + 0.1)/(X.building_acceleration_add_value + 0.1)
    X["treat_remain"] = X.treatment_acceleraion_add_value - X.treatment_acceleration_reduce_value
    X["treat_use_rate"] = (X.treatment_acceleration_reduce_value+0.1)/(X.treatment_acceleraion_add_value+0.1)
    X["res_remain"] = X.reaserch_acceleration_add_value - X.reaserch_acceleration_reduce_value
    X["res_use_rate"] = (X.reaserch_acceleration_reduce_value+ 0.1)/(X.reaserch_acceleration_add_value+ 0.1)
    #X.loc[X.avg_online_minutes == 0,"avg_acce_add"] = 0
    bd_cols_lv = [col for col in X.columns if col.startswith("bd")]
    sr_cols_lv = [col for col in X.columns if col.startswith("sr")]
    X["pve_vs_price"] = X["pve_win_count"]/(X["pay_price"]+0.1 )
    X["pvp_vs_price"] = X["pvp_win_count"]/(X["pay_price"]+0.1 )
    X["total_bd_lv"] = X[bd_cols_lv].sum(axis=1)
    X["total_sr_lv"] = X[sr_cols_lv].sum(axis=1)
    X["total_lv"] = X["total_bd_lv"] + X["total_sr_lv"]
    X["sr_prod_lv"] = X[['sr_rss_a_prod_levell','sr_rss_b_prod_level','sr_rss_c_prod_level','sr_rss_d_prod_level']].sum(axis=1)
    X["ivory_use_rate"] = (X["ivory_reduce_value"] + 0.1)/(X["ivory_add_value"] + 0.1)
    X["ivory_remain"] = X["ivory_add_value"] - X["ivory_reduce_value"]
