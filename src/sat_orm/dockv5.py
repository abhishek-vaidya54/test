"""
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier

CLASSIFICATION: 
            Highly Sensitive

    **** Add Contributors name if you have contributed to this file ****
*********************************************************************************

DESCRIPTION:
            The dockv5_orm package is a presentation of the orms for the dockv5
            schema. As the table schema is deliccate and can affect other
            files when changes, the goal of the orm is to match with the
            schema at all times, meaning that we can now represent the 
            dockv5 schema as lines of code.
            
            +---------------+
            | Dockv5 Tables |
            +---------------+
            | config        |
            | dock_phase    |
            +---------------+

            **** Edit This File If tables are added or removed ****
"""
from sat_orm.dockv5_orm.dockv5_base import get_session

from sat_orm.dockv5_orm.config import Config
from sat_orm.dockv5_orm.dock_phase import DockPhase

from sat_orm.dockv5_orm.firmware import Firmware
from sat_orm.dockv5_orm.firmware_group import FirmwareGroup
from sat_orm.dockv5_orm.firmware_group_association import FirmwareGroupAssociation
from sat_orm.dockv5_orm.hardware import Hardware
from sat_orm.dockv5_orm.device_type import DeviceType

from sat_orm.dockv5_orm.marshmallow import schemas as Schemas
