class DiffConfig():
    def __init__(self, labs, submissions_dir, solutions_dir, rosters_dir, results_dir,
                 csv_path, csv_name, score_out_of, roster_paths):
        self.labs = labs
        self.submissions_dir = submissions_dir
        self.solutions_dir = solutions_dir
        self.rosters_dir = rosters_dir
        self.results_dir = results_dir

        self.csv_header = 'First,Last,Email,' + str(labs)[1:-1].replace(' ', '')
        self.csv_path = csv_path
        self.csv_name = csv_name

        self.score_out_of = float(score_out_of)
        self.roster_paths = roster_paths


class DiffResult():
    def __init__(self):
        self.result = {}

    def __str__(self):
        return str(self.result)

    def add_entry(self, author_name, result):
        if author_name not in self.result:
            self.result[author_name] = result
        else:
            self.result[author_name].update(result)

    def add_author(self, author_name):
        self.result[author_name] = {}

    def add_authors(self, author_names):
        for author_email in author_names:
            self.add_author(author_email)

    def add_result(self, author_name, lab, result):
        if author_name not in self.result:
            self.result[author_name] = {}
        self.result[author_name][lab] = result

