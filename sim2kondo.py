import numpy as np
def jointdata():
    # % Joint angles at uprighht posture (Trim)  and  Directions of rotation from robot servo vs robot simulation
    n = 17;
    q2dir = np.zeros(n);
    q_trim = np.ones(n);
    q_id = np.zeros(n, dtype=int);
    q_sio = np.zeros(n, dtype=int);
    # Head
    q_id[0] = 0;
    q_sio[0] = 1;
    q2dir[0] = -1;
    q_trim[0] = 0;
    # % Left hand
    q_id[1:4] = [1, 2, 4];
    q_sio[1:4] = [1, 1, 1];
    q2dir[1:4] = [-1, +1, +1];
    q_trim[1:4] = [np.pi / 2, 0, 0];
    # % Right hand
    q_id[4:7] = [1, 2, 4];
    q_sio[4:7] = [2, 2, 2];
    q2dir[4:7] = [+1, +1, -1];
    q_trim[4:7] = [np.pi / 2, 0, 0];
    # % Left leg
    q_id[7:12] = [6, 7, 8, 9, 10];
    q_sio[7:12] = [1, 1, 1, 1, 1];
    q2dir[7:12] = [+1, -1, +1, +1, -1];
    q_trim[7:12] = [-np.pi / 2, 0, 0, 0, 0];
    # % Right leg
    q_id[12:17] = [6, 7, 8, 9, 10];
    q_sio[12:17] = [2, 2, 2, 2, 2];
    q2dir[12:17] = [+1, +1, -1, -1, -1];
    q_trim[12:17] = [-np.pi / 2, 0, 0, 0, 0];
    return n,q_id,q_sio,q2dir,q_trim

