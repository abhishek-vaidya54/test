"""glcc_haptic

Revision ID: ff505328a1a3
Revises: 153896d3e27d
Create Date: 2021-05-05 09:46:57.215658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ff505328a1a3"
down_revision = "153896d3e27d"
branch_labels = None
depends_on = None


def upgrade():
    settings_json_denton = """{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": true, "athleteEnabled": false,"showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 1, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 0, "showSafetyScoreModal": true, "exposureHapticEnabled": true, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 70, "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [267]:
        sql = """insert into settings (value, target_type, target_id) values ('{0}', 'warehouse', {1})""".format(
            settings_json_denton, warehouse
        )
        op.execute(sql)

    settings_json_glcc1 = """{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": true, "athleteEnabled": false,"showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 5, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 499800, "showSafetyScoreModal": true, "exposureHapticEnabled": true, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 75, "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [241]:
        sql = """insert into settings (value, target_type, target_id) values ('{0}', 'warehouse', {1})""".format(
            settings_json_glcc1, warehouse
        )
        op.execute(sql)

    settings_json_glcc2 = """{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": true, "athleteEnabled": false,"showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 5, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 600000, "showSafetyScoreModal": true, "exposureHapticEnabled": true, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 75, "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [242]:
        sql = """insert into settings (value, target_type, target_id) values ('{0}', 'warehouse', {1})""".format(
            settings_json_glcc2, warehouse
        )
        op.execute(sql)

    settings_json_wm = """{"handsFree": false, "eulaVersion": null, "enableMotion": true, "hapticEnabled": false, "athleteEnabled": false,"showEngagement": true, "enableProximity": false, "showHapticModal": true, "enagementEnabled": true, "hapticBendNumber": 1, "enableTemperature": true, "exposureRSSILimit": -48, "hapticFeedbackGap": 0, "showBaselineModal": false, "showSafetyJudgement": true, "hapticBendPercentile": 50, "hapticFeedbackWindow": 0, "showSafetyScoreModal": true, "exposureHapticEnabled": true, "exposureHapticRepeatMS": 10000, "hapticSingleBendWindow": 600, "hapticSagAngleThreshold": 70, "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    for warehouse in [
        82,
        98,
        99,
        100,
        101,
        102,
        103,
        104,
        156,
        162,
        166,
        167,
        176,
        177,
        178,
        183,
        184,
        185,
        186,
        187,
    ]:
        sql = """insert into settings (value, target_type, target_id) values ('{0}', 'warehouse', {1})""".format(
            settings_json_wm, warehouse
        )
        op.execute(sql)

    settings_json_groupa_canada = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
        "enagementEnabled": true,
        "hapticBendNumber": 2,
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
        "hapticSagAngleThreshold": 65,
        "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    print(settings_json_groupa_canada)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 207);""".format(
        settings_json_groupa_canada
    )

    print(sql)
    op.execute(sql)

    settings_json_groupb_canada = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
        "enagementEnabled": true,
        "hapticBendNumber": 2,
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

    print(settings_json_groupb_canada)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 208);""".format(
        settings_json_groupb_canada
    )

    print(sql)
    op.execute(sql)

    settings_json_groupc_canada = """{"handsFree": false,
        "eulaVersion": null,
        "enableMotion": true,
        "hapticEnabled": true,
        "athleteEnabled": true,
        "showEngagement": false,
        "enableProximity": false,
        "showHapticModal": false,
        "enagementEnabled": true,
        "hapticBendNumber": 3,
        "enableTemperature": true,
        "exposureRSSILimit": -48,
        "hapticFeedbackGap": 0,
        "showBaselineModal": false,
        "showSafetyJudgement": true,
        "hapticBendPercentile": 50,
        "hapticFeedbackWindow": 480000,
        "showSafetyScoreModal": true,
        "exposureHapticEnabled": false,
        "exposureHapticRepeatMS": 10000,
        "hapticSingleBendWindow": 600,
        "hapticSagAngleThreshold": 65,
        "exposureHapticSuppressMS": 30000}""".replace(
        "\n", ""
    )

    print(settings_json_groupc_canada)
    sql = """insert into settings (value, target_type, target_id) values ('{0}','group', 209);""".format(
        settings_json_groupc_canada
    )

    print(sql)
    op.execute(sql)

    op.execute(
        """
            UPDATE industrial_athlete SET group_id=207  WHERE id in (70990, 70989, 70988, 70987, 70986, 70985, 70984, 70983, 66094, 66093, 66092, 66091, 66090, 66089, 66088, 66087, 66086, 66085, 66084, 66083, 66082, 66081, 66080, 66079, 66078, 66077, 66076, 66075, 66074, 66073, 66072, 66071, 66070, 66069, 66068, 66067, 66066, 66065, 66064, 66063, 66062, 66061, 66060, 66059, 66058, 66057, 66056, 66055, 66054, 66053, 66052, 66051, 66050, 66049, 66048, 66047, 66046, 66045, 66044, 66043, 66042, 66041, 66040, 66039, 66038, 66037, 66036, 66035, 66034, 66033, 66032, 66031, 66030, 66029, 66028, 66027, 66026, 66025, 66024, 66023, 66022, 66021, 66020, 66019, 66018, 66017, 66016, 66015, 66014, 66013, 66012, 66011, 66010, 66009, 66008, 66007, 66006, 66005, 66004, 66003, 66002, 66001, 66000, 65999, 65998, 65997, 65996, 65995, 65994, 65993);
        """
    )

    op.execute(
        """
            UPDATE industrial_athlete SET group_id=208  WHERE id in (65992, 65991, 65990, 65989, 65988, 65987, 65986, 65985, 65984, 65983, 65982, 65981, 65980, 65979, 65978, 65977, 65976, 65975, 65974, 65973, 65972, 65971, 65970, 65969, 65968, 65967, 65966, 65965, 65964, 65963, 65962, 65961, 65960, 65959, 65958, 65957, 65956, 65955, 65954, 65953, 65952, 65951, 65950, 65949, 65948, 65947, 65946, 65945, 65944, 65943, 65942, 65941, 65940, 65939, 65938, 65937, 65936, 65935, 65934, 65933, 65932, 65931, 65930, 65929, 65928, 65927, 65926, 65925, 65924, 65923, 65922, 65921, 65920, 65919, 65918, 65917, 65916, 65915, 65914, 65913, 65912, 65911, 65910, 65909, 65908, 65907, 65906, 65905, 65904, 65903, 65902, 65901, 65900, 65899, 65898, 65897, 65896, 65895, 65894, 65893, 65892, 65891, 65890, 65889, 65888, 65887, 65886, 65885, 65884, 65883);
        """
    )

    op.execute(
        """
            UPDATE industrial_athlete SET group_id=209  WHERE id in (65882, 65881, 65880, 65879, 65878, 65877, 65876, 65875, 65874, 65873, 65872, 65871, 65870, 65869, 65868, 65867, 65866, 65865, 65864, 65863, 65862, 65861, 65860, 65859, 65858, 65857, 65856, 65855, 65854, 65853, 65852, 65851, 65850, 65849, 65848, 65847, 65846, 65845, 65844, 65843, 65842, 65841, 65840, 65839, 65838, 65837, 65836, 65835, 65834, 65833, 65832, 65831, 65830, 65829, 65828, 65827, 65826, 65825, 65824, 65823, 65822, 65821, 65820, 65819, 65818, 65817, 65816, 65815, 65814, 65813, 65812, 65811, 65810, 65809, 65808, 65807, 65806, 65805, 65804, 65803, 65802, 65801, 65800, 65799, 65798, 65797, 65796, 65795, 65794, 65793, 65792, 65791, 65790, 65789, 65788, 65787, 65786, 65785, 65784, 65783, 65782, 65781, 65780, 65779, 65778, 65777, 65776, 65775, 65774);
        """
    )


def downgrade():
    pass
