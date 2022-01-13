"""RDC_split_test

Revision ID: b42664120d3d
Revises: 0f578005ca5c
Create Date: 2021-05-07 11:36:07.331579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b42664120d3d"
down_revision = "0f578005ca5c"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            UPDATE groups SET override_settings=1 WHERE id in (210,211,212,213);
        """
    )

    settings_json_groupa_caselot = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
        "enagementEnabled": true,
        "hapticBendNumber": 5,
        "enableTemperature": true,
        "exposureRSSILimit": -48,
        "hapticFeedbackGap": 0,
        "showBaselineModal": false,
        "showSafetyJudgement": true,
        "hapticBendPercentile": 50,
        "hapticFeedbackWindow": 300000,
        "showSafetyScoreModal": true,
        "exposureHapticEnabled": false,
        "exposureHapticRepeatMS": 10000,
        "hapticSingleBendWindow": 600,
        "hapticSagAngleThreshold": 65,
        "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    print(settings_json_groupa_caselot)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 210);""".format(
        settings_json_groupa_caselot
    )

    print(sql)
    op.execute(sql)

    settings_json_groupb_caselot = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
        "enagementEnabled": true,
        "hapticBendNumber": 4,
        "enableTemperature": true,
        "exposureRSSILimit": -48,
        "hapticFeedbackGap": 0,
        "showBaselineModal": false,
        "showSafetyJudgement": true,
        "hapticBendPercentile": 50,
        "hapticFeedbackWindow": 300000,
        "showSafetyScoreModal": true,
        "exposureHapticEnabled": false,
        "exposureHapticRepeatMS": 10000,
        "hapticSingleBendWindow": 600,
        "hapticSagAngleThreshold": 70,
        "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    print(settings_json_groupb_caselot)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 211);""".format(
        settings_json_groupb_caselot
    )

    print(sql)
    op.execute(sql)

    settings_json_groupa_noncon = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
        "enagementEnabled": true,
        "hapticBendNumber": 5,
        "enableTemperature": true,
        "exposureRSSILimit": -48,
        "hapticFeedbackGap": 0,
        "showBaselineModal": false,
        "showSafetyJudgement": true,
        "hapticBendPercentile": 50,
        "hapticFeedbackWindow": 600000,
        "showSafetyScoreModal": true,
        "exposureHapticEnabled": false,
        "exposureHapticRepeatMS": 10000,
        "hapticSingleBendWindow": 600,
        "hapticSagAngleThreshold": 75,
        "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    print(settings_json_groupa_noncon)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 212);""".format(
        settings_json_groupa_noncon
    )

    print(sql)
    op.execute(sql)

    settings_json_groupb_noncon = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
        "enagementEnabled": true,
        "hapticBendNumber": 5,
        "enableTemperature": true,
        "exposureRSSILimit": -48,
        "hapticFeedbackGap": 0,
        "showBaselineModal": false,
        "showSafetyJudgement": true,
        "hapticBendPercentile": 50,
        "hapticFeedbackWindow": 300000,
        "showSafetyScoreModal": true,
        "exposureHapticEnabled": false,
        "exposureHapticRepeatMS": 10000,
        "hapticSingleBendWindow": 600,
        "hapticSagAngleThreshold": 70,
        "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    print(settings_json_groupb_noncon)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 213);""".format(
        settings_json_groupb_noncon
    )

    print(sql)
    op.execute(sql)

    op.execute(
        """
            UPDATE industrial_athlete SET group_id=210  WHERE id in (68544, 68542, 68539, 68537, 68538, 68536, 68540, 68533, 68531, 68532, 68534, 68528, 68529, 68530, 70733, 70732, 68526, 68525, 68527, 68568, 70731, 68522, 68521, 68524, 68520, 68523, 68565, 68563, 68547, 68589, 70708, 68706, 68707, 68708, 70722, 70721, 68673, 68675, 68674, 68672, 68631, 68630, 68629, 68733, 68731, 68588, 68585, 68587, 68586, 70707, 70706, 68705, 68704, 68702, 68703, 70720, 68670, 68671, 68625, 68627, 68626, 68730, 68580, 68584, 68583, 68582, 68581, 68579, 70705, 68701, 68700, 68699, 68698, 70718, 70719, 68667, 68666, 68668, 68669, 68622, 68624, 68623, 68621, 68729, 68575, 68578, 68576, 68574, 68577, 68697, 68696, 70717, 70716, 68665, 68663, 68664, 68662, 68616, 68620, 68618, 68617, 68619, 68727, 68728, 68725, 68726, 68570, 68571, 68569, 68573, 68572, 68693, 68695, 68692, 68694, 70715, 68661, 68660, 68659, 68657, 68656, 68658, 68614, 68613, 68611, 68612);
        """
    )

    op.execute(
        """
            UPDATE industrial_athlete SET group_id=211  WHERE id in (68566, 68564, 68562, 70730, 70729, 68517, 68518, 68514, 68515, 68519, 68516, 68560, 68561, 68558, 68559, 68557, 70728, 68512, 68513, 68511, 68554, 68552, 68556, 68553, 68555, 68551, 68550, 68548, 68549, 68615, 68722, 68723, 68721, 68724, 68690, 68691, 70714, 68655, 68654, 68651, 68653, 68652, 68609, 68610, 68720, 68719, 68689, 70713, 68650, 68606, 68608, 68607, 68716, 68717, 68687, 68688, 68686, 70712, 68647, 68649, 68648, 68605, 68601, 68600, 68604, 68603, 68711, 68713, 68712, 68714, 70726, 68683, 68682, 68684, 68685, 68646, 68643, 68645, 68644, 68642, 68743, 68744, 68596, 68599, 68598, 68597, 70711, 68710, 70724, 70725, 68681, 68680, 68678, 68679, 68641, 68636, 68637, 68640, 68638, 68639, 68628, 68742, 68740, 68739, 68741, 68592, 68593, 68594, 68590, 68595, 68591, 70710, 70709, 68709, 70723, 68677, 68676, 68635, 68633, 68634, 68632, 68735, 68738, 68736, 68737, 68734);
        """
    )

    op.execute(
        """
            UPDATE industrial_athlete SET group_id=212  WHERE id in (68496, 68497, 68498, 68499, 68500, 70698, 68495, 68494, 68492, 68493, 68489, 68491, 68490, 68488, 70704, 68487, 70703, 68486, 68485, 70701, 70702, 68483, 68484, 68481, 68464, 68465, 68466, 68427, 68462, 68463, 68461, 68460, 68426, 68424, 68423, 68425, 68457, 68459, 68458, 68455, 68456, 68421, 68419, 68418, 68420, 68453, 33333, 68452, 68415, 68417, 68413, 68416, 68414, 68450, 68451);
        """
    )

    op.execute(
        """
            UPDATE industrial_athlete SET group_id=213  WHERE id in (68482, 70700, 68479, 68480, 68477, 68478, 68510, 68472, 68474, 68473, 68475, 68509, 68508, 68468, 68469, 68470, 68507, 68506, 68505, 70699, 68501, 68503, 68502, 68504, 68449, 68448, 68410, 68411, 68412, 68409, 68408, 68407, 68446, 68443, 68444, 68445, 68447, 70727, 68440, 68441, 68439, 68442, 68405, 68437, 68434, 68436, 68435, 68438, 68467, 68433, 68430, 68432, 68431, 68429, 68428);
        """
    )


def downgrade():
    pass
