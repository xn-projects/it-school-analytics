import pandas as pd

class DataSummary:
    """
    Utility class for generating a quick overview of a pandas DataFrame.
    """
    def __init__(self, name, df):
        self.name = name
        self.df = df

    def summary_info(self):
        print('Dataset name: ', self.name)
        print(f'Rows: {self.df.shape[0]}, Colums: {self.df.shape[1]}')

        col_types = pd.Series({col:self.df[col].dtype for col in self.df.columns})
        col_uniques = pd.Series({col:self.df[col].unique()[:5] for col in self.df.columns})

        column_types = {}
        for col in self.df.columns:
            dtype = self.df[col].dtype

            if pd.api.types.is_numeric_dtype(dtype):
                column_types[col] = 'numeric'

            elif pd.api.types.is_datetime64_any_dtype(dtype):
                column_types[col] = 'datetime'

            elif pd.api.types.is_categorical_dtype(dtype):
                cat_dtype = self.df[col].cat.categories.dtype
                column_types[col] = f'category ({cat_dtype})'

            elif pd.api.types.is_string_dtype(dtype):
                column_types[col] = 'string'

            elif dtype == object:
                object_types = self.df[col].map(type).dropna().unique()
                type_names = [t.__name__ for t in object_types]
                if len(type_names) == 1:
                    column_types[col] = f'object ({type_names[0]})'
                else:
                    column_types[col] = f'object (mixed: {", ".join(type_names)})'

            else:
                column_types[col] = str(dtype)

        summary_info = pd.DataFrame ({
            'non_nulls': self.df.count(),
            'nulls': self.df.isna().sum(),
            'null_pct': (self.df.isna().mean() * 100).round(2),
            'dtype': col_types,
            'column_type': col_types.index.map(column_types.get),
            'nunique': self.df.nunique(),
            'sample_values': col_uniques
        })

        summary_info = summary_info[
            [
                'non_nulls',
                'nulls',
                'null_pct',
                'dtype',
                'column_type',
                'nunique',
                'sample_values'
            ]
        ]

        return summary_info
