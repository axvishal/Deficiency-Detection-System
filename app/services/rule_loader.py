# Redis disabled for local development

DEFAULT_RULES = {
    "capacity_mw": {"type": "tolerance", "tolerance": 5, "critical": True},
    "total_investment_cr": {"type": "tolerance", "tolerance": 10, "critical": False},
    "plot_area_ha": {"type": "tolerance", "tolerance": 10, "critical": False},
    "project_name": {"type": "exact", "critical": True}
}

def load_rules():
    return DEFAULT_RULES
