'''本文件暂时做尝试过思路的草稿了'''

# valid_venue = event_df[event_df.venue_id.notnull()]
# valid_weekday = valid_venue[valid_venue.weekday == now_weekday]
# valid_clock = valid_weekday[valid_weekday.clock == now_clock]
# valid_e = list(valid_clock['event_id'])
# print("get_choices:%d" % len(valid_e))

# df = open('src/ltmp_vars/tmp.pkl', 'wb')
# pickle.dump(user_df, df, True)
# pickle.dump(ueg_df, df, True)
# df.close()

# ueg_df['sum'] = 1
# conflict_cnt = ueg_df.groupby(['group_id', 'clock_h', 'weekday', 'event_id'], as_index=False)['sum'].agg({'count': np.sum})
# conflict_cnt['sum'] = 1
# conflict_cnt = conflict_cnt.groupby(['group_id', 'clock_h', 'weekday'], as_index=False)['sum'].agg({'count': np.sum})
# conflict_cnt['sum'] = 1
# conflict_cnt = conflict_cnt.groupby(['group_id', 'clock_h'], as_index=False)['sum'].agg({'count': np.sum})
# conflict_cnt['sum'] = 1
# conflict_cnt = conflict_cnt.groupby(['group_id'], as_index=False)['sum'].agg({'count': np.sum})
# conflict_group_cnt = conflict_cnt[conflict_cnt['count']>1]
