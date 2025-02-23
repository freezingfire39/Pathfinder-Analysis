from rest_framework import serializers

class OptimizationInputSerializer(serializers.Serializer):
    symbols = serializers.ListField(child=serializers.CharField())
    amount = serializers.FloatField()
    method = serializers.ChoiceField(choices=[('equally_weighted', 'Equally Weighted'),
                                              ('min_volatility', 'Minimal Volatility'),
                                              ('max_sharpe_ratio', 'Max Sharpe Ratio')])

class CustomWeightSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    weight = serializers.FloatField()
class CustomInputSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    weights = CustomWeightSerializer(many=True)

class OptimizedPortfolioSerializer(serializers.Serializer):
    fund = serializers.CharField()
    weight = serializers.FloatField()
    amount = serializers.FloatField()

class TimeSeriesSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    value = serializers.FloatField()

class PortfolioSerializer(serializers.Serializer):
    component = OptimizedPortfolioSerializer(many=True)
    returns = TimeSeriesSerializer(many=True)

class AnalysisSerializer(serializers.Serializer):
    type = serializers.CharField()
    values = TimeSeriesSerializer(many=True)

class ScoreSerializer(serializers.Serializer):
    type = serializers.CharField()
    value = serializers.FloatField()

class AnalyzerOutputSerializer(serializers.Serializer):
    portfolio = PortfolioSerializer()
    analysis = AnalysisSerializer(many=True)
    score = ScoreSerializer(many=True)