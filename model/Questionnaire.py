class Questionnaire:
    def __init__(self, questions, answer_recs, filter_rec, object_id, filename):
        self.questions = questions
        self.answer_recs = answer_recs
        self.filter_rec = filter_rec
        self._id = object_id
        self.filename = filename
