from model import CovidModel, PeopleGroup
from utils import SimpleGroup, BasicStatistics

################################################################################
# Common parameters amongst all scenarios

# COVID model

mask_user_rate = 0.0
mask_efficacy = 0.0
imune_rate = 0.01
initial_infection_rate = 0.01
hospitalization_capacity = 0.02
latency_period_mean = 3.0
latency_period_stdev = 1.0
incubation_period_mean = 7.0
incubation_period_stdev = 4.0
disease_period_mean = 20
disease_period_stdev = 5

# Population group

daily_interaction_count = 4
contagion_probability = 0.2
asymptomatic_isolation_rate = 0.0
symptomatic_isolation_rate = 0.0

# Simulation

population_size = 1000
simulation_cycles = 90 # days

################################################################################
# Scenarios

scenario = {}

# ------------------------------------------------------------------------------

sc = 1 # Do nothing
scenario[sc] = {}
scenario[sc]['model'] = CovidModel(
    mask_user_rate = mask_user_rate,
    mask_efficacy = mask_efficacy,
    imune_rate = imune_rate,
    initial_infection_rate = initial_infection_rate,
    hospitalization_capacity = hospitalization_capacity,
    latency_period_mean = latency_period_mean,
    latency_period_stdev = latency_period_stdev,
    incubation_period_mean = incubation_period_mean,
    incubation_period_stdev = incubation_period_stdev,
    disease_period_mean = disease_period_mean,
    disease_period_stdev = disease_period_stdev
)
scenario[sc]['group'] = SimpleGroup(0, scenario[sc]['model'], population_size,
    daily_interaction_count = daily_interaction_count,
    contagion_probability = contagion_probability,
    asymptomatic_isolation_rate = asymptomatic_isolation_rate,
    symptomatic_isolation_rate = symptomatic_isolation_rate
)

# ------------------------------------------------------------------------------

sc = 2 # Restrict the mobility only for infected people
scenario[sc] = {}
scenario[sc]['model'] = CovidModel(
    mask_user_rate = mask_user_rate,
    mask_efficacy = mask_efficacy,
    imune_rate = imune_rate,
    initial_infection_rate = initial_infection_rate,
    hospitalization_capacity = hospitalization_capacity,
    latency_period_mean = latency_period_mean,
    latency_period_stdev = latency_period_stdev,
    incubation_period_mean = incubation_period_mean,
    incubation_period_stdev = incubation_period_stdev,
    disease_period_mean = disease_period_mean,
    disease_period_stdev = disease_period_stdev
)
scenario[sc]['group'] = SimpleGroup(0, scenario[sc]['model'], population_size,
    symptomatic_isolation_rate = 0.9,
    asymptomatic_isolation_rate = asymptomatic_isolation_rate,
    daily_interaction_count = daily_interaction_count,
    contagion_probability = contagion_probability
)

# ------------------------------------------------------------------------------

sc = 3 # restrict the mobility for everybody
scenario[sc] = {}
scenario[sc]['model'] = CovidModel(
    mask_user_rate = mask_user_rate,
    mask_efficacy = mask_efficacy,
    imune_rate = imune_rate,
    initial_infection_rate = initial_infection_rate,
    hospitalization_capacity = hospitalization_capacity,
    latency_period_mean = latency_period_mean,
    latency_period_stdev = latency_period_stdev,
    incubation_period_mean = incubation_period_mean,
    incubation_period_stdev = incubation_period_stdev,
    disease_period_mean = disease_period_mean,
    disease_period_stdev = disease_period_stdev
)
scenario[sc]['group'] = SimpleGroup(0, scenario[sc]['model'], population_size,
    symptomatic_isolation_rate = 0.9,
    asymptomatic_isolation_rate = 0.8,
    daily_interaction_count = daily_interaction_count,
    contagion_probability = contagion_probability
)

# ------------------------------------------------------------------------------

sc = 4 # Restrict the mobility after 10% of the population being infected
       # and release the restrictions when more then 95% is safe

       # This scenarios illustrates the use of listeners to change simulation
       # parameters during the simulation based in some dynamic criterion

class IsolationRule():
    def __init__(self, group, perc1, perc2):
        self.perc1 = perc1
        self.perc2 = perc2
        self.group = group
        self.state = 0
    def start_cycle(self, model):
        pass
    def end_cycle(self, model):
        if self.state == 0:
            if (group.infected_count / group.size) >= self.perc1:
                self.state = 1
                group.symptomatic_isolation_rate = 0.9
                group.asymptomatic_isolation_rate = 0.8
        elif self.state == 1:
            if (group.infected_count / group.size) <= (1.0 - self.perc2):
                self.state = 2
                group.symptomatic_isolation_rate = 0.0
                group.asymptomatic_isolation_rate = 0.0

scenario[sc] = {}
sc4_model = CovidModel(
    mask_user_rate = mask_user_rate,
    mask_efficacy = mask_efficacy,
    imune_rate = imune_rate,
    initial_infection_rate = initial_infection_rate,
    hospitalization_capacity = hospitalization_capacity,
    latency_period_mean = latency_period_mean,
    latency_period_stdev = latency_period_stdev,
    incubation_period_mean = incubation_period_mean,
    incubation_period_stdev = incubation_period_stdev,
    disease_period_mean = disease_period_mean,
    disease_period_stdev = disease_period_stdev
)
sc4_group = SimpleGroup(0, sc4_model, population_size,
    symptomatic_isolation_rate = 0.0,
    asymptomatic_isolation_rate = 0.0,
    daily_interaction_count = daily_interaction_count,
    contagion_probability = contagion_probability
)
sc4_model.add_listener(IsolationRule(sc4_group, 0.1, 0.95))
scenario[sc]['model'] = sc4_model
scenario[sc]['group'] = sc4_group

################################################################################
# Simulation of all scenarios

for sc in scenario:
    model = scenario[sc]['model']
    group = scenario[sc]['group']
    statistics = BasicStatistics(model)
    model.add_group(group)
    model.add_listener(statistics)
    for i in range(simulation_cycles):
        model.step()
    statistics.export_chart("scenario" + str(sc) + ".png")
    statistics.export_csv("scenario" + str(sc) + ".csv")