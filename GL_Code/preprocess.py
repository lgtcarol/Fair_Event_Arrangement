import pandas as pd
import numpy as np
import os
import json

def json2csv(data_path,dest,filename, type='event'):
    if type=='event':
        try:
            with open(data_path, 'r') as fr:
                content = json.load(fr)['results']
            df = pd.DataFrame(columns=['city','topics','lat','lon', 'id'])
            for i in range(len(content)):
                #if not topics == "":
                    #topics = eval(content[i]['topics'])
                    #topics = topics['name']
                tmp_content = content[i]
                topics = tmp_content['topics']
                tpcs = ''
                if not topics == []:
                    for i in range(len(topics)):
                        tpcs += topics[i]['name']+' '
                else:
                    tpcs = ''

                row = pd.DataFrame({'city': [content[i]['city']],
                                    'topics': [tpcs],
                                    'lat': [content[i]['lat']],
                                    'lon': [content[i]['lon']],
                                    'id': [tmp_content['id']]
                                    })
                df = df.append(row, ignore_index=True)
                #df.drop_duplicates()
            df.to_csv(dest+filename + str('.csv'), index=False)

        except IOError as e:
            print('File%s not found. Exit.'% data_path)
            return
        pass

def extract_rsvp(source, r_file):
    content = pd.read_csv(source + r_file)
    #print(content)
    if len(content) > 0:
        rsvp = pd.DataFrame(content, columns=['member', 'response'])
        rsvp['member'] = rsvp['member'].map(lambda s: eval(s)['member_id'])
        rsvp['event_id'] = r_file[5:-4]
    group_id = eval(content['group'][0])['id']
    print(group_id)
    return rsvp, group_id


def batch_extract_rsvp(source, files, dest):
    res = pd.DataFrame(columns=['event_id', 'member', 'response'])
    event_group = pd.DataFrame()
    try:
        for p in files:
            rsvp, group_id = extract_rsvp(source, p)
            res = res.append(rsvp, ignore_index=True)
            event_group = event_group.append({'event_id':p[5:-4], 'group_id': group_id}, ignore_index=True)
            event_group.drop_duplicates()
            print(str(p) + ' finished... ')
    except pd.errors.EmptyDataError:
        print('Exists one empty data error!')


    res.to_csv(dest+'rsvp.csv', index=False)
    event_group.to_csv(dest+'event_group.csv', index=False)
    print('The extraction finished.')
    pass


def extract_member(m_file):
    content = pd.read_csv(m_file)
    #print(content.head())
    #content['topics'].map(lambda s : s[1:-1])
    members = pd.DataFrame(content, columns=['id', 'topics'])
    #members['topics'].map(lambda l: eval(l)['name'])
    count = 0
    def tpc_trans(topics):
        if topics == '[]' or topics == np.nan:
            return ''
        try:
            topics = eval(str(topics))
        except NameError as e:
            print('name "nan" is not defined')
            return ''
        tpcs = ''
        if not topics == []:
            #if topics == 'topics'
            try:
                for i in range(len(topics)):
                    tpcs += topics[i]['name'] + ' '
            except TypeError as e:
                print(str(topics)+ " string indices must be integers!")
        else:
            tpcs = ''
        return tpcs

    #members['topics'] = members['topics'].map(tpc_trans)
    members['topics']= members['topics'].apply(tpc_trans)
    try:
        members['topics'] = members['topics'].replace({'': np.nan})
    except TypeError as e:
        print('TypeError ignored... ')
    #print(members.head())
    real = members.dropna()
    #real.to_csv('~/Downloads/Chicago/members/%s_real.csv'% m_file[39:-4], index=False)
   # members.to_csv('~/Downloads/Chicago/members/%s.csv'%m_file[39:-4], index=False)
    return real, members

    pass


def batch_extract_member(paths, dest):
    real_merge = pd.DataFrame(columns=['id', 'topics'])
    all_merge = pd.DataFrame(columns=['id', 'topics'])
    for p in paths:
        real, members = extract_member(p)
        real_merge = real_merge.append(real, ignore_index=True).drop_duplicates()
        all_merge = all_merge.append(members, ignore_index=True).drop_duplicates()
        print(str(p) + ' finished... ')

    real_merge.to_csv(dest+'labeled_members.csv', index=False)
    all_merge.to_csv(dest+'all_members.csv', index=False)
    pass


def extract_event_conflict(e_file, setting='minv'):

    content = pd.read_csv(e_file)
    conf = pd.DataFrame(content, columns=['id', 'time', 'duration'])

    """
    Default duration setting skill:
    Inside one group, to fill the NaN value of duration with a certain duration of events in this group:
    1. default: min value 
    2. average value
    3. mode value
    4. median value
    5. max value
    """
    print(len(conf))
    print(len(conf.dropna()))

    avg = conf['duration'].dropna().mean()
    minv = conf['duration'].dropna().min()
    maxv = conf['duration'].dropna().max()
    modv = conf['duration'].dropna().mode()
    mdnv = conf['duration'].dropna().median()
    print(avg, minv, modv, mdnv, maxv)

    real = conf.dropna()

    if setting == 'avg':
        adpt = conf['duration'].fillna(avg)
    elif setting == 'modv':
        adpt = conf['duration'].fillna(modv)
    elif setting == 'mdnv':
        adpt = conf['duration'].fillna(mdnv)
    elif setting == 'maxv':
        adpt = conf['duration'].fillna(maxv)
    else:
        adpt = conf['duration'].fillna(minv)


    print(adpt.head())
    adpt.to_csv('~/Downloads/Chicago/event_conflict_%s/adapt_%s.csv'% (setting, e_file[39:-4]), index=False)
    real.to_csv('~/Downloads/Chicago/event_conflict_%s/real_%s.csv' % (setting, e_file[39:-4]), index=False)
    return real, adpt
    pass


def batch_extract_event_conflict(paths,dest_dir, setting='minv'):
    real_merge = pd.DataFrame(columns=['id', 'time', 'duration'])
    adpt_merge = pd.DataFrame(columns=['id', 'time', 'duration'])
    try:
        for p in paths:
            real, adpt = extract_event_conflict(p, setting)
            #real_merge = real_merge.append(real, ignore_index=True)
            #adpt_merge = adpt_merge.append(adpt, ignore_index=True)
            print(str(p) + 'finished... ')
    except TypeError as e:
        print(e + " ignored... ")

    #real_merge.to_csv(dest_dir+'real.csv', index=False)
    #adpt_merge.to_csv(dest_dir+'adpt.csv', index=False)

    pass

def extract_event():
    pass


def find_events_path(p):
    cand = os.listdir(p)
    #filter(lambda s : s[:6]=='events', cand)
    res = [e for e in cand if e[:6] == 'events']
    return res


def find_rsvp_path(p):
    cand = os.listdir(p)
    #filter(lambda s : s[:4]=='rsvp', cand)
    res = [e for e in cand if e[:4] == 'rsvp']
    return res


def find_member_path(p):
    cand = os.listdir(p)
    #filter(lambda s : s[:6]=='member', cand)
    res = [e for e in cand if e[:6] == 'member']
    return res


if __name__=="__main__":
    path = '/Users/apple/Downloads/LA/LA/'

    #print(find_events_path(path)[:5])

    #print(len(find_rsvp_path(path)))
    e_path = [path+e for e in find_events_path(path)]
    #print(len(e_path))

    path1 = path + 'events_10250542.csv'

    #extract_event_conflict(path1)
    #batch_extract_member(path, )
    #batch_extract_rsvp()

    #path2 = '~/Downloads/Chicago/event_conflict_minv/'
    #batch_extract_event_conflict(e_path, path2, setting='minv')
    #path2 = '~/Downloads/LA/event_conflict_mdnv/'
    #batch_extract_event_conflict(e_path, path2, setting='mdnv')
    #path2 = '~/Downloads/LA/event_conflict_maxv/'
    #batch_extract_event_conflict(e_path, path2, setting='maxv')

    path = '/Users/apple/Downloads/LA/LA/'
    m_path = [path+e for e in find_member_path(path)]
    #path2 = path + 'member_10787332.csv'
    #print(extract_member(path2))
    path3 = '~/Downloads/LA/members/'
    batch_extract_member(m_path, dest=path3)

    #r_path = find_rsvp_path(path)
    #path4 = path + 'rsvp_231882878.csv'
    #extract_rsvp(path, 'rsvp_231882878.csv')
    #batch_extract_rsvp(path, r_path, dest='~/Downloads/Chicago/rsvp/')

    #json_filepath = './data/json_members/'
    #file_name = 'members6'
    #json2csv(json_filepath+file_name+str('.json'), dest='./data/', filename=file_name)
