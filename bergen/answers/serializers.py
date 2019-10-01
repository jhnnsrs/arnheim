from rest_framework import serializers

from answers.models import Answer, Oracle, Answering, Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class OracleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oracle
        fields = "__all__"


class AnsweringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answering
        fields = "__all__"
