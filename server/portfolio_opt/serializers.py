from rest_framework import serializers

class OptimizationInputSerializer(serializers.Serializer):
    symbols = serializers.ListField(child=serializers.CharField())
    amount = serializers.FloatField()
    method = serializers.ChoiceField(choices=[('equally_weighted', 'Equally Weighted'),
                                              ('minimal_volatility', 'Minimal Volatility'),
                                              ('max_sharpe_ratio', 'Max Sharpe Ratio')])

class OptimizedPortfolioSerializer(serializers.Serializer):
    fund = serializers.CharField()
    weight = serializers.FloatField()
    amount = serializers.FloatField()

class TimeSeriesSerializer(serializers.Serializer):
    date = serializers.DateField()
    value = serializers.FloatField()

class PortfolioSerializer(serializers.Serializer):
    component = serializers.ListField(child=OptimizedPortfolioSerializer())
    returns = serializers.ListField(child=TimeSeriesSerializer())