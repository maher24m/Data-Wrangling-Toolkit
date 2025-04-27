import pandas as pd


class DataCleaningFactory:
    """Just a marker / interface – every cleaner implements .apply(df, **params)."""
    def apply(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        raise NotImplementedError


class MissingValuesCleaner(DataCleaningFactory):
    def apply(self, df: pd.DataFrame,
              method: str,
              columns: list[str] | None = None,
              value=None,
              **kwargs
              ) -> pd.DataFrame:
        cols = columns or list(df.columns)
        if method == "mean":
            for c in cols:
                df[c] = df[c].fillna(df[c].mean())
        elif method == "median":
            for c in cols:
                df[c] = df[c].fillna(df[c].median())
        elif method == "mode":
            for c in cols:
                m = df[c].mode()
                if not m.empty:
                    df[c] = df[c].fillna(m[0])
        elif method == "constant":
            if value is None:
                raise ValueError("constant replacement requires a 'value' parameter")
            df = df.fillna({c: value for c in cols})
        else:
            raise ValueError(f"Unknown method '{method}' for missing_values")
        return df


class RemoveDuplicatesCleaner(DataCleaningFactory):
    def apply(self, df: pd.DataFrame,
              columns: list[str] | None = None,
              keep: str = "first",
              **kwargs
              ) -> pd.DataFrame:
        return df.drop_duplicates(subset=columns, keep=keep)


class RemoveMissingCleaner(DataCleaningFactory):
    def apply(self, df: pd.DataFrame,
              how: str = "any",
              subset: list[str] | None = None,
              **kwargs
              ) -> pd.DataFrame:
        return df.dropna(how=how, subset=subset)


class DetectOutliersCleaner(DataCleaningFactory):
    def apply(self, df: pd.DataFrame,
              method: str = "std",
              n_std: float = 3,
              columns: list[str] | None = None,
              **kwargs
              ) -> pd.DataFrame:
        cols = columns or df.select_dtypes(include="number").columns
        mask = pd.Series(False, index=df.index)
        if method == "std":
            for c in cols:
                m, s = df[c].mean(), df[c].std()
                mask |= (df[c] < m - n_std * s) | (df[c] > m + n_std * s)
        elif method == "iqr":
            for c in cols:
                q1, q3 = df[c].quantile([0.25, 0.75])
                iqr = q3 - q1
                mask |= (df[c] < q1 - 1.5 * iqr) | (df[c] > q3 + 1.5 * iqr)
        else:
            raise ValueError(f"Unknown method '{method}' for detect_outliers")
        df[f"_is_outlier"] = mask
        return df


class ReplaceOutliersCleaner(DataCleaningFactory):
    def apply(self, df: pd.DataFrame,
              method: str = "std",
              n_std: float = 3,
              replace_with: str = "mean",
              columns: list[str] | None = None,
              **kwargs
              ) -> pd.DataFrame:
        # First flag them
        flagged = DetectOutliersCleaner().apply(df.copy(), method=method, n_std=n_std, columns=columns)
        cols = columns or df.select_dtypes(include="number").columns
        # compute replacement stats
        stats = {}
        for c in cols:
            if replace_with == "mean":
                stats[c] = df[c].mean()
            elif replace_with == "median":
                stats[c] = df[c].median()
            elif replace_with == "mode":
                m = df[c].mode()
                stats[c] = m[0] if not m.empty else df[c].mean()
            else:
                raise ValueError(f"Unknown replace_with '{replace_with}'")
        mask = flagged["_is_outlier"]
        for c in cols:
            df.loc[mask, c] = stats[c]
        return df.drop(columns=["_is_outlier"])


class StandardizeFormatCleaner(DataCleaningFactory):
    def apply(self, df: pd.DataFrame,
              date_columns: list[str] | None = None,
              number_columns: list[str] | None = None,
              **kwargs
              ) -> pd.DataFrame:
        for c in date_columns or []:
            df[c] = pd.to_datetime(df[c], errors="coerce")
        for c in number_columns or []:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        return df


class ClusterSimilarCleaner(DataCleaningFactory):
    def apply(self, df: pd.DataFrame,
              column: str,
              threshold: float = 0.8,
              **kwargs
              ) -> pd.DataFrame:
        # stub – no-op
        return df
