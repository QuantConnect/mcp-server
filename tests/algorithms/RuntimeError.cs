#region imports
    using System;
    using QuantConnect.Algorithm;
#endregion
public class BacktestRuntimeErrorTestAlgorithm : QCAlgorithm
{
    public override void Initialize()
    {
        throw new Exception("Test");
    }
}