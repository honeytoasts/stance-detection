# rm -rf model
# rm -rf tensorboard

python train.py \
    --experiment_no 1 \
    --evaluate_nli 0 \
    --model task-specific-shared \
    --max_seq_len 20 \
    --embedding wikipedia \
    --nli_dataset_size 0.1 \
    --stance_output_dim 3 \
    --nli_output_dim 3 \
    --embedding_dim 300 \
    --stance_hidden_dim 128 \
    --nli_hidden_dim 128 \
    --shared_hidden_dim 128 \
    --stance_linear_dim 100 \
    --nli_linear_dim 100 \
    --shared_linear_dim 100 \
    --num_stance_rnn 1 \
    --num_nli_rnn 1 \
    --num_shared_rnn 1 \
    --num_stance_gcn 1 \
    --num_nli_gcn 1 \
    --num_shared_gcn 1 \
    --num_stance_linear 1 \
    --num_nli_linear 1 \
    --attention linear \
    --attention_threshold 0.1 \
    --rnn_dropout 0.3 \
    --gcn_dropout 0.3 \
    --linear_dropout 0.5 \
    --nli_loss_weight 1.0 \
    --learning_rate 5e-5 \
    --weight_decay 0 \
    --clip_grad_value 1.0 \
    --lr_decay_step 10 \
    --lr_decay 1 \
    --random_seed 77 \
    --kfold 5 \
    --test_size 0.2 \
    --epoch 50 \
    --batch_size 16