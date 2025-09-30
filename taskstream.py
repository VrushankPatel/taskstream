"""TaskStream dataset loader for Hugging Face"""

import json
import yaml
from pathlib import Path
import datasets

_DESCRIPTION = """
TaskStream is a comprehensive dataset of enterprise business workflows, decision-making processes, 
organizational structures, and operational documentation across multiple industries.
"""

_HOMEPAGE = "https://github.com/yourusername/taskstream"

_LICENSE = "apache-2.0"

class TaskStream(datasets.GeneratorBasedBuilder):
    """TaskStream: Enterprise Workflow Dataset"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="workflows",
            version=VERSION,
            description="Business workflow processes (YAML)"
        ),
        datasets.BuilderConfig(
            name="decisions", 
            version=VERSION,
            description="Decision scenarios and outcomes (JSON)"
        ),
        datasets.BuilderConfig(
            name="communications",
            version=VERSION,
            description="Business communications examples (Markdown)"
        ),
        datasets.BuilderConfig(
            name="all",
            version=VERSION,
            description="All content categories combined"
        ),
    ]

    DEFAULT_CONFIG_NAME = "all"

    def _info(self):
        if self.config.name == "workflows":
            features = datasets.Features({
                "id": datasets.Value("string"),
                "title": datasets.Value("string"),
                "content": datasets.Value("string"),
                "category": datasets.Value("string"),
                "industry": datasets.Value("string"),
            })
        elif self.config.name == "decisions":
            features = datasets.Features({
                "id": datasets.Value("string"),
                "content": datasets.Value("string"),
                "category": datasets.Value("string"),
                "industry": datasets.Value("string"),
            })
        elif self.config.name == "communications":
            features = datasets.Features({
                "id": datasets.Value("string"),
                "content": datasets.Value("string"),
                "category": datasets.Value("string"),
                "industry": datasets.Value("string"),
            })
        else:  # all
            features = datasets.Features({
                "id": datasets.Value("string"),
                "content": datasets.Value("string"),
                "category": datasets.Value("string"),
                "industry": datasets.Value("string"),
                "file_type": datasets.Value("string"),
            })

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        # No splits - this is a single corpus
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"config_name": self.config.name},
            ),
        ]

    def _generate_examples(self, config_name):
        """Yields examples."""
        idx = 0
        
        categories = {
            "workflows": ("workflows", ".yaml"),
            "decisions": ("decisions", ".json"),
            "communications": ("communications", ".md"),
            "org_structures": ("org_structures", ".md"),
            "metrics": ("metrics", ".md"),
            "policies": ("policies", ".md"),
        }
        
        if config_name == "all":
            cats_to_process = categories.items()
        elif config_name in categories:
            cats_to_process = [(config_name, categories[config_name])]
        else:
            cats_to_process = categories.items()
        
        for cat_name, (directory, extension) in cats_to_process:
            cat_path = Path(directory)
            if not cat_path.exists():
                continue
                
            for file in cat_path.glob(f"*{extension}"):
                try:
                    content = file.read_text(encoding='utf-8')
                    industry = file.stem.split('_')[0]
                    
                    example = {
                        "id": file.stem,
                        "content": content,
                        "category": cat_name,
                        "industry": industry,
                    }
                    
                    if config_name == "all":
                        example["file_type"] = extension
                    
                    yield idx, example
                    idx += 1
                    
                except Exception as e:
                    print(f"Error loading {file}: {e}")
                    continue
