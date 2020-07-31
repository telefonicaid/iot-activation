### Table of Contents
- [Telit IoT Portal](#telit-iot-portal)
  * [SIMs Connections](#sims-connections)
  * [SIMs Activation](#sims-activation)
  * [Identify the APN](#identify-the-apn)
- [Next steps](#next-steps)


# Kite Platform

If you have been accepted into the program, in a few days you will receive a development kit with a set of SIM cards.

You will be eager to start playing with it, but first of all you must make sure that the SIM cards are activated and you have access 
to the management platform.


## SIMs Connections

In Kite Platform (Kite_Platform.md) you can access the connectivity management portal and manage all your SIM.

# How to get started with your SIM

1. First of all, your SIM must be [assigned to a subscription group](Kite_Platform.md#assign-subscription-group)
2. In order for a SIM to be operational, it must be in [activated state](Kite_Platform.md#change-life-cycle-state)
3. You must make sure that the SIM has the [data traffic activated](Kite_Platform.md#activate-data-traffic)
4. And lastly Identify the APN (Kite_Platform.md#select-apn)

There are many more options and [services available](Kite_Platform.md#how-its-made) for your SIM

## Learn about life cycle state

For connect your SIM need to be operational. for it, the SIM must be activated.
Follow the diagram below

![pic](pictures/Kite/Kite_interface_SIM_LifeCycle.png)

- **Inactive new**: initial state of any SIM card. The card will remain in this state until you 
assign a Subscription Group to it (including a commercial plan).

- **Test**: optional and available test for once the SIM card is assigned to a
Subscriptions group that takes into account that state in its commercial plan.
This state enables a limited traffic in order to prove the SIM card is functioning
correctly.

- **Activation ready**: previous state to Activated and state the SIM card changes to
once the time or the available traffic is consumed in the Test state.

- **Pending activation**: It is a state similar to the previous one, but in this one the change
to the Activated state is done manually from Inventory.

- **Activated**: In this state the SIM card is fully operating.

- **Deactivated**: In this state, the SIM card does not have traffic but its permanence
can entail an associated fee. From this state, the card can be activated again
manually.

- **Suspended**: This is used typically in cases of fraud or unpaid.

- **Retired**: This state will always be the last.. This state can only be reached if the card is suspended.
Once in this state, there is no going back. 

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)



# Next steps

Now your SIM is activated and you know everything you need to know to make it work.

Your next step is to insert it into your device and start developing.

- [Telit's Bravo Evaluation Kit](Telit_Bravo.md)

- [other development kits boards...](IoT_Activation_boards.md)

