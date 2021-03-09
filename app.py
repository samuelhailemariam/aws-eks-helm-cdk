from aws_cdk import (
    aws_iam as _iam,
    aws_eks as _eks,
    aws_ec2 as _ec2,
    core
)


class EkscdkStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        primaryRegion = core.Environment(region='us-west-2')
        
        clusterAdmin = _iam.Role(
            self, 'AdminRole',
            assumed_by = _iam.AccountRootPrincipal(),
        )
        
        cluster = _eks.Cluster(
            self, 'demo-cluster',
            cluster_name = 'demo',
            masters_role = clusterAdmin,
            version = _eks.KubernetesVersion.V1_18,
            default_capacity = 2,
        )
        
        cluster.add_auto_scaling_group_capacity(
            'spot-group',
            instance_type = _ec2.InstanceType('t3.medium'),
            spot_price = '0.248' if core.Stack.region == 'primaryRegion' else '0.192'
        )

        cluster.add_helm_chart(
            'apache',
            repository = 'https://charts.bitnami.com/bitnami',
            chart = 'apache',
            release = 'apache'
        )

app = core.App()
EkscdkStack(app, "ekscdk", env={'region': 'us-west-2'})

app.synth()