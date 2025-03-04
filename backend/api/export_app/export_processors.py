from django.http import HttpResponse
import pandas as pd
import io

class BaseExportProcessor:
    """Base class for export processors."""
    @staticmethod
    def export(df, dataset_name):
        raise NotImplementedError("Subclasses must implement 'export' method.")

class CSVExportProcessor(BaseExportProcessor):
    """Handles CSV file export."""
    @staticmethod
    def export(df, dataset_name):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{dataset_name}.csv"'
        df.to_csv(path_or_buf=response, index=False)
        return response

class ExcelExportProcessor(BaseExportProcessor):
    """Handles Excel file export."""
    @staticmethod
    def export(df, dataset_name):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)
        response = HttpResponse(output.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f'attachment; filename="{dataset_name}.xlsx"'
        return response
class JSONExportProcessor(BaseExportProcessor):
    """Handles JSON file export."""
    @staticmethod
    def export(df, dataset_name):
        response = HttpResponse(content_type="application/json")
        response["Content-Disposition"] = f'attachment; filename="{dataset_name}.json"'
        response.write(df.to_json(orient="records"))
        return response

class ExportProcessorFactory:
    """Factory to get the right export processor based on file type."""
    processors = {
        "csv": CSVExportProcessor,
        "excel": ExcelExportProcessor,
        "json": JSONExportProcessor,
    }

    @staticmethod
    def get_processor(file_type):
        if file_type in ExportProcessorFactory.processors:
            return ExportProcessorFactory.processors[file_type]
        raise ValueError(f"Unsupported export format: {file_type}")

    @staticmethod
    def register_processor(file_type, processor_class):
        """Allows users to add a new file format processor dynamically."""
        if not issubclass(processor_class, BaseExportProcessor):
            raise TypeError("Processor must inherit from BaseExportProcessor")
        ExportProcessorFactory.processors[file_type] = processor_class
