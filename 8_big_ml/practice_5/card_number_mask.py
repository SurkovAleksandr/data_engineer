# Описание задания - https://lab.karpov.courses/learning/355/module/3437/lesson/30465/85652/401560/
import numpy as np
import pandas as pd
from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql.types import StringType


@pandas_udf(StringType(), PandasUDFType.SCALAR)
def card_number_mask(nc: pd.Series) -> pd.Series:
    return nc.str.slice_replace(start=4, stop=12, repl='*')


arr = np.array(['4034954837458345', '4876954837458345'])
s = pd.Series(['4034954837458345', '4876954837458345'])
print(s)
print(card_number_mask(s))