def save_results(results, filename):
    with open(filename, 'w') as outfile:
        json.dump(results, outfile, default=to_json)
        print('SAVED: {0!s}'.format(filename))
