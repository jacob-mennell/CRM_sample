#Candidate
def candidate_trim(data):
    '''
    Cleaning function for candidate table

    Arguments:
        # data - dataframe containing raw data pulled from API (pd.dataframe object)

    Return:
        # data - cleaned data (pd.dataframe object)
    '''
    # Ensure empty date rows are set to 0
    data['dateAdded'].iloc[data['dateAdded'].isnull()] = 0
    data['dateLastModified'].iloc[data['dateLastModified'].isnull()] = 0

    # flatten all the json datatypes if else is used for the case that it is empty
    data['city'] = data['address'].apply(lambda x: x['city'])
    data['country'] = data['address'].apply(lambda x: x['countryName'] if len(x) != 0 else x)
    data['category_id'] = data['category'].apply(
        lambda x: x['id'] if x != None else None)
    data['category_name'] = data['category'].apply(
        lambda x: x['name'] if x != None else None)
    data['owner_id'] = data['owner'].apply(
        lambda x: x['id'] if x != None else None)
    data["company_name"] = data["companyName"].apply(lambda x: ",".join(x) if type(x) == list else x)
    data["employment_preference"] = data["employmentPreference"].apply(lambda x: ",".join(x) if type(x) == list else x)

    # DATES - The unixtime formats need to be converted to UTC timestamp
    data['date_added'] = data['dateAdded'].apply(
        lambda x: datetime.utcfromtimestamp(int(x) / 1000).strftime('%Y-%m-%d %H:%M:%S'))
    data['date_added'] = pd.to_datetime(data['date_added'], format='%Y-%m-%d %H:%M:%S')
    data['date_last_modified'] = data['dateLastModified'].apply(
        lambda x: datetime.utcfromtimestamp(int(x) / 1000).strftime('%Y-%m-%d %H:%M:%S'))
    data['date_last_modified'] = pd.to_datetime(data['date_last_modified'], format='%Y-%m-%d %H:%M:%S')

    # formatting interviews
    data['interview_total'] = data['interviews'].apply \
        (lambda x: x['total'] if x['total'] > 0 else 0)
    data['interview_id1'] = data['interviews'].apply \
        (lambda x: x['data'][0]['id'] if x['total'] > 0 else None)
    data['interview_id2'] = data['interviews'].apply \
        (lambda x: x['data'][1]['id'] if x['total'] > 1 else None)
    data['interview_id3'] = data['interviews'].apply \
        (lambda x: x['data'][2]['id'] if x['total'] > 2 else None)
    data['interview_id4'] = data['interviews'].apply \
        (lambda x: x['data'][3]['id'] if x['total'] > 3 else None)
    data['interview_id5'] = data['interviews'].apply \
        (lambda x: x['data'][4]['id'] if x['total'] > 4 else None)

    # location data
    data["desired_locations"] = data["desiredLocations"].apply(lambda x: ", ".join(x) if type(x) == list else x)
    data["desired_locations"] = data["desired_locations"].str.title()

    # Minor data cleaning with regex
    data['desired_locations'] = data['desired_locations'].str.replace(r'(.*Leicestershire.*)', 'Wimbledon')
    data['desired_locations'] = data['desired_locations'].str.replace(r'(.*ondon.*)', 'Wimbledon')
    data['desired_locations'] = data['desired_locations'].str.replace(r'(.*Aberdeenshire.*)', 'Wimbledon')
    data['desired_locations'] = data['desired_locations'].str.replace(r'(.*Uk.*)', 'Wimbledon')
    data['desired_locations'] = data['desired_locations'].str.replace(r'(.*Leicestershire.*)', 'Wimbledon')

    # Drop the old columns and rename Primary Key column
    data.drop(columns=['address',
                       'interviews',
                       'dateAdded',
                       'dateLastModified',
                       'category',
                       'owner',
                       'employmentPreference',
                       'companyName',
                       'desiredLocations',
                       '_score'],
              inplace=True)
    data.rename(columns={'id': 'candidate_id',
                         'firstName': 'first_name',
                         'lastName': 'last_name',
                         }, inplace=True)
    return data
